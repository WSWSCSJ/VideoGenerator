from service.constants import Color, Size


class BaseConfigure:
    """
    pictures/audio: multi file use request.FILES.getlist(argument_key)
    """
    video_attributes = (
        "fps", "frames", "step", "length",
        "size", "video_format", "render"
    )
    audio_attributes = (
        "start", "end", "audio_format"
    )
    integer_keys = ("fps", "frames", "step", "length", "start", "end")
    media_keys = ("pictures", "audio")
    string_keys = ("render", "video_format")
    object_keys = ("color", "size")
    extra_keys = ("audio_format", )
    all = integer_keys + media_keys + string_keys + object_keys + extra_keys
    fps = 30
    frames = 20
    step = 1
    length = 20
    color = Color.WHITE
    size = Size.size
    render = "default"
    start = 0
    end = 20
    video_format = "mp4"
    audio_format = "mp3"
    pictures = []
    audio = []

    def __str__(self):
        return '\n'.join(['%s:%s' % item for item in self.__dict__.items()])


class Handler(BaseConfigure):

    def __init__(self, request):
        self.request = request
        self.serializer()

    def serializer(self):
        r = self.request

        for key in self.integer_keys + self.string_keys:
            _ = r.get_argument_no_error(key)
            if _ and key in self.integer_keys:
                setattr(self, key, int(_))
            if _ and key in self.string_keys:
                setattr(self, key, str(_))

            color = r.get_argument_no_error('color')
            if color:
                assert type(color) == str
                if color not in Color.all:
                    raise ValueError("color error, not such color as '{}'".format(color))
                self.color = Color.get(color)

            size = r.get_argument_no_error('size')
            if size:
                assert type(size) == str
                sizes = size.split("X")
                if len(sizes) != 2:
                    raise ValueError("size value error should be '123X456'")
                self.size = (int(sizes[0]), int(sizes[1]))

            audio = r.request.files.get("audio")
            if not audio or len(audio) != 1:
                raise ValueError("audio can only be set as one")
            self.audio = audio[0].get('body')
            self.audio_format = audio[0].get('filename').split(".")[-1]

            pictures = r.request.files.get("pictures")
            if not pictures or len(pictures) == 0:
                raise ValueError("pictures can't be null")
            self.pictures = [_.get('body') for _ in pictures]
