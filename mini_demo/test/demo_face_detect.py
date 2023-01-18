import logging
import asyncio


from mini.apis.errors import get_vision_error_str
from mini.apis.api_observe import ObserveFaceDetect
from mini.apis.api_sence import FaceDetect, FaceAnalysis, ObjectRecognise, ObjectRecogniseType, TakePicture, \
    FaceRecognise, GetInfraredDistance, GetRegisterFaces, TakePictureType
from mini.apis.api_sound import StartPlayTTS
from mini.dns.dns_browser import WiFiDevice
from mini.pb2.codemao_facedetecttask_pb2 import FaceDetectTaskResponse
import test_connect
import mini.mini_sdk as MiniSdk


'''
async def test_ObserveFaceDetect():
    """
    Face count detection demo

    Face count detection, if a face is detected, an event will be reported

    When the number of detected faces is greater than or equal to 1, 
    stop monitoring and broadcast "There seems to be xx faces in front of me" (xx is the number of faces)

    """
    observer: ObserveFaceDetect = ObserveFaceDetect()

    # FaceDetectTaskResponse.count
    # FaceDetectTaskResponse.isSuccess
    # FaceDetectTaskResponse.resultCode
    def handler(msg: FaceDetectTaskResponse):
        print(f"{msg}")
        if msg.isSuccess and msg.count:
            observer.stop()
            asyncio.create_task(__tts(msg.count))

    observer.set_handler(handler)
    observer.start()
    await asyncio.sleep(0)


async def __tts(count):
    await StartPlayTTS(text=f' in front of me there seems to be{count} personal').execute()
    asyncio.get_running_loop().run_in_executor(None, asyncio.get_running_loop().stop)
'''


# Test face detection
async def test_face_detect():
    """
    test face count detection
    Detect the number of faces, 10s timeout, and wait for a response.
    #FaceDetectResponse.count : number of faces
    #FaceDetectResponse.isSuccess : Success or Not
    #FaceDetectResponse.resultCode : Return Code

    """
    # timeout: Specify the duration of the detection
    block: FaceDetect = FaceDetect(timeout=10)
    # response: FaceDetectResponse
    (resultType, response) = await block.execute()

    print(f'test_face_detect result: {response}')


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
    print('code = {0}, error={1}'.format(response.resultCode, get_vision_error_str(response.resultCode)))


# Test object recognition: flower recognition, 10s timeout
async def test_object_recognise_flower():
    """
    Test object (flower) recognition
    Have the robot identify the flower
    (you have to manually put the flower or a photo of the flower in front of the robot), time out for 10s,
    and wait for the results
    #RecogniseObjectResponse.objects : array of object names [str]
    #RecogniseObjectResponse.isSuccess : whether or not it succeeds
    #RecogniseObjectResponse.resultCode : Return Code

    """
    # object_type: Supports FLOWER, FRUIT, GESTURE
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FLOWER, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_recognise_flower result: {response}')


# Test object recognition: identify fruit, 10s timeout
async def test_object_recognise_fruit():
    """
    Test object (fruit) recognition
    Have the robot identify the flower
    (you have to manually put the fruit or a picture of the fruit in front of the robot), time out for 10s,
    and wait for the result
    #RecogniseObjectResponse.objects : array of object names [str]
    #RecogniseObjectResponse.isSuccess : whether or not it succeeds
    #RecogniseObjectResponse.resultCode : Return Code

    """
    # object_type: Supports FLOWER, FRUIT, GESTURE objects.
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.FRUIT, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_recognise_fruit result: {response}')


# Test object recognition: gesture recognition, 10s timeout
async def test_object_recognise_gesture():
    """
    test object (gesture) recognition
    Get the robot to recognize the flower (you have to manually gesture in front of the robot), time out for 10s,
    and wait for the result.
    #RecogniseObjectResponse.objects : array of object names [str]
    #RecogniseObjectResponse.isSuccess : whether or not it succeeds
    #RecogniseObjectResponse.resultCode : Return Code

    """
    # object_type: Supports FLOWER, FRUIT, GESTURE
    block: ObjectRecognise = ObjectRecognise(object_type=ObjectRecogniseType.GESTURE, timeout=10)
    # response : RecogniseObjectResponse
    (resultType, response) = await block.execute()

    print(f'test_object_recognise_gesture result: {response}')


# Test photography
async def test_take_picture():
    """
    test_take_picture()
    Have the robot take pictures immediately and wait for the results
    #TakePictureResponse.isSuccess : Success or Not
    #TakePictureResponse.code : return code
    #TakePictureResponse.picPath : The path where the photo is stored in the bot.

    """
    # response: TakePictureResponse
    # take_picture_type: IMMEDIATELY-immediately, FINDFACE-find the face and take the picture.
    (resultType, response) = await TakePicture(take_picture_type=TakePictureType.IMMEDIATELY).execute()

    print(f'test_take_picture result: {response}')


# Testing facial recognition
async def test_face_recognise():
    """
    test face recognition
    Have the robot perform face recognition inspection, time out 10s, and wait for the results
    #FaceRecogniseResponse.faceInfos : [FaceInfoResponse] face information array
        FaceInfoResponse.id : face id
        FaceInfoResponse.name : name, default name is "stranger" if it's a stranger
        FaceInfoResponse.gender : Gender
        FaceInfoResponse.age : Age
    #FaceRecogniseResponse.isSuccess : whether or not successful
    #FaceRecogniseResponse.resultCode : Return Code
    Returns:

    """
    # response : FaceRecogniseResponse
    (resultType, response) = await FaceRecognise(timeout=10).execute()

    print(f'test_face_recognise result: {response}')


# Test to acquire infrared detection distance
async def test_get_infrared_distance():
    """
    test_infrared_distance_detection
    Get the IR distance detected by the current robot and wait for the result.
    #GetInfraredDistanceResponse.distance : Infrared distance

    """
    # response: GetInfraredDistanceResponse
    (resultType, response) = await GetInfraredDistance().execute()

    print(f'test_get_infrared_distance result: {response}')


# Test to get the number of faces currently registered in the bot
async def test_get_register_faces():
    """
    Test gets registered faces information
    Get all the faces registered in the bot and wait for the results.
    #GetRegisterFacesResponse.faceInfos : [FaceInfoResponse] face information array
        #FaceInfoResponse.id : face id
        #FaceInfoResponse.name : Name
        #FaceInfoResponse.gender : gender
        #FaceInfoResponse.age : age
    #GetRegisterFacesResponse.isSuccess : whether it succeeds or not
    #GetRegisterFacesResponse.resultCode : Return Code
    Returns:

    """
    # reponse : GetRegisterFacesResponse
    (resultType, response) = await GetRegisterFaces().execute()

    print(f'test_get_register_faces result: {response}')


async def main():

    await test_connect.test_get_device_by_name()
    client: WiFiDevice = await test_connect.test_get_device_by_name()
    print("Client: ", client)
    client = await test_connect.test_connect(client)

    await test_connect.test_start_run_program()
    await test_face_detect()
    await test_face_analysis()
    await test_object_recognise_flower()
    await test_object_recognise_fruit()
    await test_object_recognise_gesture()
    await test_take_picture()
    await test_face_recognise()
    await test_get_infrared_distance()
    await test_get_register_faces()
    await test_connect.shutdown()

if __name__ == '__main__':
    MiniSdk.set_log_level(logging.DEBUG)
    MiniSdk.set_robot_type(MiniSdk.RobotType.EDU)
    asyncio.run(main())
