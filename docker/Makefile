IMAGE = hypermodern-python.io

run: image
	docker run --rm --tty --interactive $(IMAGE)

image:
	docker build --tag=$(IMAGE) --progress=plain .
