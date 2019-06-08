from main.data.Youtube import Youtube

youtube = Youtube(
    [
        "AIzaSyCDH_-bK082drQl4dENR_eGYyRmS4Na7zQ"
        "AIzaSyDrEvdW_Hu-0BtqmciIow-q14shuKxhhXc",
        "AIzaSyCYvwIEVDJpL89W6qqEbI_EyVVijC_6e2Q"
    ]
)
while True:
    youtube.related(
        "",
        "",
        2,
        "",
        1,
        ""
    )