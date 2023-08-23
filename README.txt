Thank you for Downloading My Program! :)

Introduction:
    This simple python add uses tkinter to create a GUI that interfaces with the 
    pytube package to create a simple youtube downloader. The program is designed by me, Karl. 

Download Instructions:
    1. Please verify that you have these python packages: pytube, tkinter, os, logging, pandas, and numpy.
        If you do not have all of these packages, please pip install them on your machine.
    2. clone my git files into their own folder.  

Usage Instructions:
    1. navigate to your favorite youtube video or playlist and past the URL into the 
        Input text field. 
    2. Select the desired download location by clicking the "Select Download Location" button. 
        The default value is "~/Music". 
    3. Select on either Audio Only or Video Only from the top menu. 
        The default value is "Audio Only".
    4. Check the "High Quality" radio button if high quality is desired. 
        The default value is "Low Quality".
    5. Click the "Download" button to begin the download. 
    6. The Screen will now display the download process.
    


Common Error Instructions:
    if you recieve an error titled something like this: "pytube.exceptions.RegexMatchError: get_throttling_function_name: could not find match for multiple"
    the cipher.py file in the pytube package needs to be updated. Please navigate to the cipher.py file and change 
    the regex in the function_patterns def. 
    Full code segment from github: (https://github.com/pytube/pytube/issues/1678)
        function_patterns = [
        # https://github.com/ytdl-org/youtube-dl/issues/29326#issuecomment-865985377
        # https://github.com/yt-dlp/yt-dlp/commit/48416bc4a8f1d5ff07d5977659cb8ece7640dcd8
        # var Bpa = [iha];
        # ...
        # a.C && (b = a.get("n")) && (b = Bpa[0](b), a.set("n", b),
        # Bpa.length || iha("")) }};
        # In the above case, `iha` is the relevant function name
        r'a\.[a-zA-Z]\s*&&\s*\([a-z]\s*=\s*a\.get\("n"\)\)\s*&&.*?\|\|\s*([a-z]+)',
        r'\([a-z]\s*=\s*([a-zA-Z0-9$]+)(\[\d+\])?\([a-z]\)',
    ]