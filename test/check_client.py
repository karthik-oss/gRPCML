import grpc

import model_pb2
import model_pb2_grpc
import pandas as pd
import pickle as cp
import base64 
def run():
	channel = grpc.insecure_channel('localhost:22222')
	df=pd.DataFrame([["hello","sello","jello"]])
	df=df.append([["gello","cello","tello"]])
	df.reset_index(drop=True,inplace=True)
	#for idx, row in df.iterrows():
	#	print (row[0],row[1])
	mm=model_pb2.msg_dataframe()
	mm.msg=df.to_json()
	proto_str=mm.SerializeToString()
	#mm.msg[:]=df.to_json()
	#mm.msg[:]=cp.dumps(df)
#		proto_str = protobuf_obj.SerializeToString()
		#return gzip.compress(proto_str)
	stub = model_pb2_grpc.EPG_MLServicesStub(channel)
	response = stub.DetectAnomalies(model_pb2.msg_dataframe(msg=df.to_json().encode('utf8')))
	#response = stub.DetectAnomalies(gzip.compress(mm))
	#response = stub.DetectAnomalies(msg_dataframe = mm)
	ndf=response.msg
	print(ndf)
	
    #print("Encdded service received:\n EnctransactionID:%s\n,Encproperties:%s\n,EncsenderID:%s\n"%(response.enctransactionID,response.encproperties,response.encsenderID))

if __name__ == "__main__":
    run()
