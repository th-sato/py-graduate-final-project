from picar_v import PicarV

picar_v = PicarV()


def commands_to_picar(request):
    if 'action' in request.GET:
        action = request.GET['action']
        if action == 'forward':
            picar_v.forward()
        elif action == 'backward':
            picar_v.backward()
        elif action == 'restart':
            picar_v.restart()
        elif action == 'stop':
            picar_v.stop_car()

    elif 'speed' in request.GET:
        speed = int(request.GET['speed'])
        picar_v.speed(speed)

    elif 'turn' in request.GET:
        turn = (int(request.GET['turn']))
        picar_v.turn(turn)

    elif 'cali_wheel' in request.GET:
        cali_wheel = request.GET['cali_wheel']
        picar_v.calibration_back_wheel(cali_wheel)
