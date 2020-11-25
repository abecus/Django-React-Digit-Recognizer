from rest_framework.decorators import api_view
from rest_framework.response import Response
from .digitRecognizer.mnist_digits import crop_and_predict
import json
import re
import base64 
import numpy as np


@api_view(["GET"])
def api_overview(request):
	api_urls = {
		"request for image recognition at": "api/recognize/",
	}
	return Response(api_urls)


@api_view(['Post'])
def recognize(request):
	try:
		body_unicode = request.body.decode("utf-8")
		body_data = json.loads(body_unicode)
		datauri = body_data.get("data", None)
		imgstr = re.search(r'base64,(.*)', datauri).group(1)
		image_data = base64.b64decode(imgstr)
		
		with open('tmp.jpg', 'wb') as f:
			f.write(image_data)

		number, prob, pred = crop_and_predict("tmp.jpg")
		print(pred.shape)
		return Response({"Number": number, "probability": prob, "predictions" : pred})
		
	except:
		return Response("Ooop somthing went wrong...")
