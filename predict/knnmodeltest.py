import pickle

# Check if you can load the model manually
with open('knn_model.pkl', 'rb') as f:
    model = pickle.load(f)
    print(model)
