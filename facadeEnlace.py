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


def encapsulate(payload):



    txLen = len(payload)
    print(txLen)
    '''
        Head = 10 bytes:
            payloadLen = 5 bytes
            EOP = 13 bytes
            stuffing = 3 bytes
    '''
    payloadLen = int_to_byte(txLen,5)
    head = bytes(payloadLen)+EOP+stuffingByte
    all = bytes()
    all += head
    all += payload
    all += EOP
    print("\n Head len:  ",len(head))
    return all

def readHeadNAll(receivedAll):
    
    head = receivedAll[0:21]
    print("head:  ",head[0:21])
    txLen = fromByteToInt(head[0:5])
    eopSystem = head[5:18]
    stuffByte = head[17:21]

    sanityCheck = []
    stuffByteCount = 0


    
    for i in range(22, len(receivedAll)):
        
        if receivedAll[i] == stuffByte:
            sanityCheck.append(receivedAll[i+1:i+13])
            stuffByteCount += 1
            i = i+13
            continue

        elif receivedAll[i:i+13] != eopSystem:
            sanityCheck.append(receivedAll[i])

        else:
            break



    if len(sanityCheck) == txLen:
        
        print ("sanityCheck = okay")
        return sanityCheck, txLen, eopSystem, stuffByte

    else:
        print ("\n\n ERRO  \n\n HOUVE FALHA NA TRANSMISSÃO. FECHANDO APLICAÇÃO… TENTE NOVAMENTE.")
        quit()





        





    



def teste():
    img = Image.open('circuit.jpg', mode='r')
    testeSubject = encapsulate(img)
    print(testeSubject)
    txLenRead, eopSystem, stufg = readHeadNAll(testeSubject)

    print("\n Reading TxLen:     ",txLenRead )
    print("\n Reading eopSystem: ", eopSystem)
    print("\n Reading Stuffing:  ", stufg)
