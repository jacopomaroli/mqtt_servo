pipenv:
	PIPENV_VENV_IN_PROJECT=1 pipenv install --python 3.9.0

act-pipenv:
	pipenv shell

install-deps:
	pipenv install adafruit-circuitpython-servokit paho-mqtt && pip install git+https://github.com/sn4k3/FakeRPi

docker-build-armv6:
	docker buildx build --platform linux/arm/v6 --load -t jacopomaroli/mqtt_servo:master -f Dockerfile .

docker-run-armv6-2:
	docker run -e QEMU_CPU=arm1176 --platform=linux/arm/v6 --rm -t jacopomaroli/mqtt_servo:master

docker-run-armv6:
	docker-compose -f docker-compose-test.yml up

docker-push:
	docker push jacopomaroli/mqtt_servo:master

save:
	docker save --output mqtt_servo.tar jacopomaroli/mqtt_servo:master

load:
	docker load --input mqtt_servo.tar