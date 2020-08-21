import os

from tencentcloud.common import credential
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.exception.tencent_cloud_sdk_exception import TencentCloudSDKException
from tencentcloud.ocr.v20181119 import ocr_client, models
try:
    cred = credential.Credential(
        "AKIDDOOAmBOWnyUq0ELNTYZP0W5Tq2ISjDjo", "0gKp38yYprnXAXgaDdmqgPr65nHUeYLs")

    httpProfile = HttpProfile()
    httpProfile.endpoint = "ocr.tencentcloudapi.com"

    clientProfile = ClientProfile()
    clientProfile.httpProfile = httpProfile
    client = ocr_client.OcrClient(cred, "ap-guangzhou", clientProfile)

    req = models.GeneralFastOCRRequest()
    req.ImageUrl = "http://139.9.90.110/a.png"
    resp = client.GeneralFastOCR(req)
    print(resp.to_json_string())

except TencentCloudSDKException as err:
    print(err)
