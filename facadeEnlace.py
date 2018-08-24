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
    
    txLen = fromByteToInt(head[0:5])
    
    eopSystem = head[5:18]
    print('END OF PACKAGE', eopSystem)
    stuffByte = head[17:21]

    sanityCheck = bytearray()
    stuffByteCount = 0


    
    for i in range(21, len(receivedAll)):
        if eopSystem == receivedAll[i:i+13]:
            print(receivedAll[i:i+13])
            break

        else:
            sanityCheck += receivedAll[i:i+1]


    print('SanityCheck ', sanityCheck)
    if len(sanityCheck) == txLen:
        
        print ("sanityCheck = okay")
        return sanityCheck, txLen

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
