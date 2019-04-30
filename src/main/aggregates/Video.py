class Video:

    def __init__(self,
                 title: str,
                 channel_title: str,
                 channel_id: str,
                 default_thumbnail: str,
                 medium_thumbnail: str,
                 high_thumbnail: str,
                 description: str,
                 published_at: str,
                 etag: str,
                 video_id: str,
                 retrieval_position: int,
                 question_id: str
                 ):

        self.title = title
        self.channelTitle = channel_title
        self.channelId = channel_id
        self.default_thumbnail = default_thumbnail
        self.medium_thumbnail = medium_thumbnail
        self.high_thumbnail = high_thumbnail
        self.description = description
        self.published_at = published_at
        self.etag = etag
        self.videoId = video_id
        self.retrievalPosition = retrieval_position
        self.questionId = question_id