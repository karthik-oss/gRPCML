from concurrent import futures
import base64
import time 

import generic_model_pb2
import generic_model_pb2_grpc

import grpc
from GenericMLModel import MLModel1
import pandas as pd
from datetime import datetime as dt

class MLServices(generic_model_pb2_grpc.GenericMLServicesServicer):

	def __init__(self):
		self.mlmodel1=''
		#Model Parameter config.
		#self.moving_window_size=4


	def ConfigureModelParameters(self, request, context):
		self.df_config=pd.read_json(request.msg)
		print(self.df_config)
		return generic_model_pb2.ack_modelupdate(updated = True)

	#def AnomalyDetectionProcess(df_train,original_metric_name,context):
	def TrainModel(self, request, context):
		df_train=pd.read_json(request.msg)
		self.mlmodel1 = MLModel1(
                      		df_train=df_train
				#,Model Parameters
                      		#window_size=self.moving_window_size
                )

		return generic_model_pb2.msg_dataframe(msg=self.mlmodel1)


    
	def InferModel(self, request, context):
		df_infer=pd.read_json(request.msg)
		#for index, row in self.df_config.iterrows():
		df_model_output=self.mlmodel1(df_infer=df_infer)

		return generic_model_pb2.msg_dataframe(msg=df_model_output.to_json())



def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    model_pb2_grpc.add_GenericMLServicesServicer_to_server(MLServices(),server)
    server.add_insecure_port('0.0.0.0:9090')
    server.start()
    try:
        while True:
            time.sleep(60*60*24)
    except KeyboardInterrupt:
        server.stop(0)

if __name__ == '__main__':
    serve()
