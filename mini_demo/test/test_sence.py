import asyncio
import logging

import mini.mini_sdk as MiniSdk

from mini.apis import errors
from mini.apis.api_sence import FaceAnalysis, FaceAnalyzeResponse
from mini.apis.api_sence import FaceDetect, FaceDetectResponse
from mini.apis.api_sence import FaceRecognise, FaceRecogniseResponse
from mini.apis.api_sence import GetInfraredDistance, GetInfraredDistanceResponse
from mini.apis.api_sence import GetRegisterFaces, GetRegisterFacesResponse
from mini.apis.api_sence import ObjectRecognise, RecogniseObjectResponse, ObjectRecogniseType
from mini.apis.api_sence import TakePicture, TakePictureResponse, TakePictureType
from mini.apis.base_api import MiniApiResultType
from mini.dns.dns_browser import WiFiDevice
from test.test_connect import test_connect, shutdown, test_start_run_program
from test.test_connect import test_get_device_by_name


# 测试人脸侦测
async def test_face_detect():
    """
    Test face count detection

    Detect the number of faces, time out in 10s, and wait for the reply result

    #FaceDetectResponse.count : Number of faces

    #FaceDetectResponse.isSuccess : Is it successful

    #FaceDetectResponse.resultCode : return code

    """
    # timeout: Specify detection duration
    block: FaceDetect = FaceDetect(timeout=10)
    # response: FaceDetectResponse
    (resultType, response) = await block.execute()

    print(f'test_face_detect result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_face_detect timetout'
    assert response is not None and isinstance(response, FaceDetectResponse), 'test_face_detect result unavailable'
    assert response.isSuccess, 'face_detect failed'


# Test face analysis (gender)
async def test_face_analysis():
    """
    Test face analysis (gender)

    Detect face information (gender, age), timeout 10s, and wait for the reply result

    When multiple people exist in front of the camera,
    return the face information with the largest proportion of the screen

    Return value: Example {"age": 24, "gender": 99, "height": 238, "width": 238}

    age: age

    gender: [1, 100], less than 50 is female, greater than 50 is male

    height: the height of the face in the camera image

    width: the width of the face in the camera screen

    """
    block: FaceAnalysis = FaceAnalysis(timeout=10)
    # response: FaceAnalyzeResponse
    (resultType, response) = await block.execute()

    print(f'test_face_analysis result: {response}')
    print('code = {0}, error={1}'.format(response.resultCode, errors.get_vision_error_str(response.resultCode)))

    assert resultType == MiniApiResultType.Success, 'test_face_analysis timetout'
    assert response is not None and isinstance(response, FaceAnalyzeResponse), 'test_face_analysis result unavailable'
    assert response.isSuccess is False, 'face_analysis failed'


# Test object recognition: identify flowers, 10s timeout
async def test_object_recognise_flower():
    """
    Test object (flower) recognition

    Let the robot recognize the flower (you need to manually put the flower or flower photo in front of the robot),
    timeout 10s, and wait for the result

    #RecogniseObjectResponse.objects : array of object names [str]

    #RecogniseObjectResponse.isSuccess : Is it successful

    #RecogniseObjectResponse.resultCode : return code

    """
    # object_type: Support FLOWER, FRUIT, GESTURE three types of objects
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FLOWER, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_recognise_flower result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_object_recognise_flower timetout'
    assert response is not None and isinstance(response, RecogniseObjectResponse), \
        'test_object_recognise_flower result unavailable '
    assert response.isSuccess is False, 'test_object_recognise_flower failed'


# Test object recognition: recognize fruit, 10s timeout
async def test_object_recognise_fruit():
    """
    Test object (fruit) recognition

    Let the robot recognize the flower
    (you need to manually put the fruit or the photo of the fruit in front of the robot),
    timeout 10s, and wait for the result

    #RecogniseObjectResponse.objects : array of object names [str]

    #RecogniseObjectResponse.isSuccess : Is it successful

    #RecogniseObjectResponse.resultCode : return code

    """
    # object_type: Support FLOWER, FRUIT, GESTURE three types of objects
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FRUIT, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_recognise_fruit result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_object_recognise_fruit timetout'
    assert response is not None and isinstance(response, RecogniseObjectResponse), \
        'test_object_recognise_fruit result unavailable'
    assert response.isSuccess is False, 'test_object_recognise_fruit failed'


# Test object recognition: recognize gestures, 10s timeout
async def test_object_recognise_gesture():
    """
    Test object (gesture) recognition

    Let the robot recognize the flower (need to manually gesture in front of the robot), timeout 10s,
    and wait for the result

    #RecogniseObjectResponse.objects : array of object names [str]

    #RecogniseObjectResponse.isSuccess : Is it successful

    #RecogniseObjectResponse.resultCode : return code

    """
    # object_type: Support FLOWER, FRUIT, GESTURE three types of objects
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.GESTURE, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_recognise_gesture result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_object_recognise_gesture timetout'
    assert response is not None and isinstance(response, RecogniseObjectResponse), \
        'test_object_recognise_gesture result unavailable'
    assert response.isSuccess is False, 'test_object_recognise_gesture failed'


# test photo
async def test_take_picture():
    """
    test photo

    Let the robot take a picture immediately and wait for the result

    #TakePictureResponse.isSuccess : Was it successful

    #TakePictureResponse.code : return code

    #TakePictureResponse.picPath : The storage path of the photo in the robot

    """
    # response: TakePictureResponse
    # take_picture_type:
    # IMMEDIATELY-take a photo immediately,
    # FINDFACE-find a face and then take a photo, two photo effects
    (resultType, response) = await TakePicture(take_picture_type=TakePictureType.IMMEDIATELY).execute()

    print(f'test_take_picture result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_take_picture timetout'
    assert response is not None and isinstance(response, TakePictureResponse), 'test_take_picture result unavailable'
    assert response.isSuccess, 'test_take_picture failed'


# Test face recognition
async def test_face_recognise():
    """
    Test face recognition

    Let the robot perform face recognition detection, timeout 10s, and wait for the result


    #FaceRecogniseResponse.faceInfos : [FaceInfoResponse] face information array

        FaceInfoResponse.id : face id

        FaceInfoResponse.name : name, if it is a stranger, the default name is "stranger"

        FaceInfoResponse.gender : gender

        FaceInfoResponse.age : Age

    #FaceRecogniseResponse.isSuccess : Is it successful

    #FaceRecogniseResponse.resultCode : return code

    Returns:

    """
    # response : FaceRecogniseResponse
    (resultType, response) = await FaceRecognise(timeout=10).execute()

    print(f'test_face_recognise result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_face_recognise timetout'
    assert response is not None and isinstance(response,
                                               FaceRecogniseResponse), 'test_face_recognise result unavailable'
    assert response.isSuccess is False, 'test_face_recognise failed'


# Test to obtain infrared detection distance
async def test_get_infrared_distance():
    """
    Test infrared distance detection

    Get the infrared distance detected by the current robot and wait for the result

    #GetInfraredDistanceResponse.distance : Infrared distance

    """
    # response: GetInfraredDistanceResponse
    (resultType, response) = await GetInfraredDistance().execute()

    print(f'test_get_infrared_distance result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_get_infrared_distance timetout'
    assert response is not None and isinstance(response, GetInfraredDistanceResponse), \
        'test_get_infrared_distance result unavailable'
    assert response.distance > 0, 'test_get_infrared_distance failed'


# Test to get the number of faces currently registered in the robot
async def test_get_register_faces():
    """
    Test to obtain registered face information

    Get all face information registered in the robot and wait for the result

    #GetRegisterFacesResponse.faceInfos : [FaceInfoResponse] face information array

        #FaceInfoResponse.id : Face ID

        #FaceInfoResponse.name : name

        #FaceInfoResponse.gender : gender

        #FaceInfoResponse.age : age

    #GetRegisterFacesResponse.isSuccess : Is it successful

    #GetRegisterFacesResponse.resultCode : return code

    Returns:

    """
    # reponse : GetRegisterFacesResponse
    (resultType, response) = await GetRegisterFaces().execute()

    print(f'test_get_register_faces result: {response}')

    assert resultType == MiniApiResultType.Success, 'test_get_register_faces timetout'
    assert response is not None and isinstance(response,
                                               GetRegisterFacesResponse), 'test_get_register_faces result unavailable'
    assert response.isSuccess, 'test_get_register_faces failed'


async def main():

    await test_get_device_by_name()
    client: WiFiDevice = await test_get_device_by_name()
    print("Client: ", client)
    await test_connect(client)

    await test_start_run_program()
    await test_face_detect()
    await test_face_analysis()
    await test_object_recognise_flower()
    await test_object_recognise_fruit()
    await test_object_recognise_gesture()
    await test_take_picture()
    await test_face_recognise()
    await test_get_infrared_distance()
    await test_get_register_faces()
    await shutdown()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
