import asyncio
from instapush import App
from datetime import datetime

# pi3 (210)로 모니터 turn on 신호를 보냅니다
@asyncio.coroutine
def tcp_echo_client(message, loop):
    reader, writer = yield from asyncio.open_connection('192.168.0.210', 9083,
                                                        loop=loop)

    print('Send: %r' % message)
    writer.write(message.encode())

    data = yield from reader.read(100)
    print('Received: %r' % data.decode())

    #print('Close the socket')
    writer.close()


#102 PC로 메세지를 보냅니다
async def push_pc(message, loop):
    fut = asyncio.open_connection('192.168.0.102', 8899,loop=loop)
    try:
        reader, writer = await asyncio.wait_for(fut, timeout=3)
    except asyncio.TimeoutError:
        print('Timeout, skipping!')
        return

    print('Send(to 102): {}'.format(message))
    writer.write(message.encode())
    writer.close()


# instapush에 push명령을 내립니다
async def push():
    cur = '9' + datetime.now().strftime('%H%M')
    app = App(appid = '595713a2a4c48ae3b8b70aa0', secret = '78fbc7d58e750b37773b3dbd13c967c5')
    app.notify(event_name = 'alarm', trackers={'msg': cur})
    #print('pushed')


#message = 'Hello World!'
message = 'moving'
loop = asyncio.get_event_loop()
loop.run_until_complete(tcp_echo_client(message, loop))
loop.run_until_complete(push())
loop.run_until_complete(push_pc('coming', loop))
loop.close()
