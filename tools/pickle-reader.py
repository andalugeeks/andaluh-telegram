import pprint
import pickle

pkl_file = '../user_data/andaluhbot_user_data'
pkl_reader = open(pkl_file, "rb")
pkl_data = pkl_reader.read()
pkl_reader.close()

user_data = pickle.loads(pkl_data)
pprint.pprint(user_data)

