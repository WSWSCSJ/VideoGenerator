# VideoGenerator
generate simple short video

### docker
```shell
# 构建镜像
docker build ./ -t video_generator
# 运行
docker run -it -p 35000:5000 --name video-generator video_generator
```