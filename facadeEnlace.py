from PIL import Image,ImageDraw
import io,os




EOP = b'/00/00/00/00'
stuffingByte = b'/7a/'


def int_to_byte(values, length):
    result = []
    for i in range(0,length):
        result.append(values >> (i*8)& 0xff)

    result.reverse()

    return result

def fromByteToInt(bytes):
    result=0

    for b in bytes:
        result=result*256+int(b)

    return result


def encapsulate(imgPayload):


    imgByteArr = io.BytesIO()
    imgPayload.save(imgByteArr, format='JPEG')
    imgByteArr = imgByteArr.getvalue()
    txLen = len(imgByteArr)
    '''
        Head = 10 bytes:
            payloadLen = 5 bytes
            EOP = 4 bytes
            stuffing = 1 byte
    '''
    payloadLen = int_to_byte(txLen,5)
    head = bytes(payloadLen)+EOP+stuffingByte
    all = bytes()
    all += head
    all += imgByteArr
    all += EOP
    print("\n Head len:  ",len(head))
    return all

def readHeadNAll(receivedAll):
    head = receivedAll[0:21]
    print("headLen:  ",head[0:5])
    txLen = fromByteToInt(head[0:5])
    eopSystem = head[5:18]
    stuffByte = head[17:21]
    return txLen, eopSystem, stuffByte



def teste():
    img = Image.open('circuit.jpg', mode='r')
    testeSubject = encapsulate(img)
    #print(testeSubject)
    txLenRead, eopSystem, stufg = readHeadNAll(testeSubject)

    print("\n Reading TxLen:     ",txLenRead )
    print("\n Reading eopSystem: ", eopSystem)
    print("\n Reading Stuffing:  ", stufg)

teste()
