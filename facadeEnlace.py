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



    bytearray = 

    for i in range(0,txLen):
        if imgByteArr[i] == EOP[0]:
            if imgByteArr[i+1] == EOP[1]:
                if imgByteArr[i+2] == EOP[2]:
                    if imgByteArr[i+3] == EOP[3]:
                        imgByteArr[i-1].append(stuffingByte)

    imgByteArr+=EOP

    '''
        Head = 10 bytes:
            payloadLen = 5 bytes
            EOP = 4 bytes
            stuffing = 1 byte
    '''
    payloadLen = int_to_byte(txLen,5)
    head = bytes(payloadLen)+EOP+stuffingByte
    all = head,imgByteArr,EOP
    print(head)

    #return all


def teste():
    img = Image.open('circuit.jpg', mode='r')
    testeSubject = encapsulate(img)
    #print(testeSubject)

teste()

print(fromByteToInt(b'\x00\x00\x00\x11\xdc'))
