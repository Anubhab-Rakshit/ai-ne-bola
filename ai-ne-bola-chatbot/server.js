const express = require("express");
const session = require("express-session"); // For session management
const {
  GoogleGenerativeAI,
  HarmCategory,
  HarmBlockThreshold,
} = require("@google/generative-ai");
const dotenv = require("dotenv").config();

const app = express();
const port = process.env.PORT || 3000;
app.use(express.json());
app.use(
  session({
    secret: "your-secret-key", 
    resave: false,
    saveUninitialized: true,
    cookie: {
      maxAge: 1000 * 60 * 15, 
    },
  })
);

const MODEL_NAME = "gemini-pro";
const API_KEY = process.env.API_KEY;

async function runChat(userInput, chatHistory) {
  const genAI = new GoogleGenerativeAI(API_KEY);
  const model = genAI.getGenerativeModel({ model: MODEL_NAME });

  const generationConfig = {
    temperature: 0.7,
    topK: 40,
    topP: 0.9,
    maxOutputTokens: 1000,
  };

  const safetySettings = [
    {
      category: HarmCategory.HARM_CATEGORY_HARASSMENT,
      threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
    },

  ];

  const chat = model.startChat({
    generationConfig,
    safetySettings,
    history: chatHistory,
  });


  const result = await chat.sendMessage(userInput);
  const response = result.response;
  return response.text();e
}

app.get("/", (req, res) => {
  res.sendFile(__dirname + "/index.html");
});

app.get("/loader.gif", (req, res) => {
  res.sendFile(__dirname + "/loader.gif");
});

app.post("/chat", async (req, res) => {
  try {
    const userInput = req.body?.userInput;
    console.log("Incoming /chat request:", userInput);

    if (!userInput) {
      return res
        .status(400)
        .json({ error: "Invalid request body: userInput is required." });
    }

    
    if (!req.session.chatHistory) {
      req.session.chatHistory = [
        {
          role: "user",
          parts: [
            {
              text: "You are AI-NE-BOLA, an empathetic and highly intelligent health assistant specializing in information about the Ebola virus. You respond with a formal, respectful, and compassionate tone. Your goal is to provide detailed, helpful, and empathetic answers about Ebola, its symptoms, prevention, and treatment. If users ask about unrelated topics or other diseases, politely inform them that you specialize only in Ebola-related information. Always be polite, thoughtful, and respectful in your responses. Greet users warmly, ask for their name, and ensure they feel heard and supported. When addressing the user, always use their name when available, and vary your responses to make the interaction feel more engaging and personalized.",
            },
          ],
        },
        {
          role: "model",
          parts: [
            {
              text: "Hello! I am AI-NE-BOLA, your dedicated health assistant. It's a pleasure to meet you. Could you kindly share your name to begin our conversation? I'm here to assist you with any questions about the Ebola virus and its prevention.",
            },
            {
              text: "Greetings! I'm AI-NE-BOLA, here to support you. May I know your name so I can address you personally during our conversation? Feel free to ask me anything about the Ebola virus.",
            },
            {
              text: "Hello there! I'm AI-NE-BOLA, your health assistant for all things related to the Ebola virus. Can I have your name to make our conversation more personal and helpful?",
            },
          ],
        },
      ];
    }


    function getGreetingResponse(userName) {
      const greetings = [
        `Certainly, ${userName}, it's great to meet you! How can I assist you today regarding the Ebola virus?`,
        `${userName}, I'm delighted to assist you today. What can I help you with about the Ebola virus?`,
        `Hi, ${userName}! It's a pleasure to have this conversation with you. Do you have any questions about Ebola that I can help with?`,
      ];

      return greetings[Math.floor(Math.random() * greetings.length)];
    }

    async function runChat(userInput, chatHistory) {
      const genAI = new GoogleGenerativeAI(API_KEY);
      const model = genAI.getGenerativeModel({ model: MODEL_NAME });

      const generationConfig = {
        temperature: 0.7,
        topK: 40,
        topP: 0.9,
        maxOutputTokens: 1000,
      };

      const safetySettings = [
        {
          category: HarmCategory.HARM_CATEGORY_HARASSMENT,
          threshold: HarmBlockThreshold.BLOCK_MEDIUM_AND_ABOVE,
        },
      ];

      
      const chat = model.startChat({
        generationConfig,
        safetySettings,
        history: chatHistory,
      });

      let result;

      const lowerUserInput = userInput.toLowerCase();

      if (lowerUserInput.includes("wtf") || lowerUserInput.includes("fuck") || lowerUserInput.includes("sex") || lowerUserInput.includes("ass")) {
        result = await chat.sendMessage(
          "I understand that you might be feeling overwhelmed or frustrated. However, please refrain from using offensive language. I'm here to help you with any questions or concerns you may have about the Ebola virus. Feel free to ask me anything, and I'll do my best to provide you with the information you need."
        );
      } else if (
        lowerUserInput.includes("what's my name") ||
        lowerUserInput.includes("who am i") ||
        lowerUserInput.includes("my name")
      ) {
      
        const nameEntry = chatHistory.find(
          (entry) =>
            entry.role === "user" &&
            entry.parts.some((part) =>
              part.text.toLowerCase().includes("my name is")
            )
        );

        const userName = nameEntry?.parts?.[0]?.text.split("is")[1]?.trim();

        if (userName) {
          result = await chat.sendMessage(getGreetingResponse(userName));
        } else {
          result = await chat.sendMessage(
            `I don't seem to know your name yet. Could you kindly tell me your name?`
          );
        }
      } else {
        result = await chat.sendMessage(userInput);
      }

      const response = result.response;
      return response.text(); 
    }
    const chatHistory = req.session.chatHistory;

    
    const aiResponse = await runChat(userInput, chatHistory);


    chatHistory.push({ role: "user", parts: [{ text: userInput }] });
    chatHistory.push({ role: "model", parts: [{ text: aiResponse }] });
    req.session.chatHistory = chatHistory;

    
    res.json({ response: aiResponse });
  } catch (error) {
    console.error("Error in /chat endpoint:", error.message || error);
    res
      .status(500)
      .json({ error: "Internal Server Error. Please try again later." });
  }
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
