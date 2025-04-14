import urllib.parse, time
import os, requests, urllib
import platform
from . import AndroidApkHex, JavaFileCode

def js_to_bookmarklet(js_code):
    # Remove leading/trailing whitespace
    js_code = js_code.strip()
    
    # Minimize code (optional: remove newlines and extra spaces)
    js_code = ' '.join(js_code.split())

    # URL encode the code
    encoded_js = urllib.parse.quote(js_code)

    # Prepend "javascript:" to make it a bookmarklet
    bookmarklet = f"javascript:{encoded_js}"
    return bookmarklet
class TinyWebapp:
    
    def __init__(self):
        if platform.system() == 'Linux':
            # Assuming Android environment
            base_url = '/storage/emulated/0/.weblauncher/'
        elif platform.system() == 'Windows':
            base_url = os.path.join(os.environ['USERPROFILE'], 'weblauncher')
        else:
            # Fallback for other OSes like macOS or Linux Desktop
            base_url = os.path.join(os.path.expanduser('~'), 'weblauncher')

        self.base_url = base_url
        self.t = time.time()
        try:
            open(base_url)
        except:
            print(f"Exception: Please Install The App , use function get_app to install [android] or get java file by get_java and compile it manually according to your systems")
            return
    def get_app(self, output_filename="based.apk"):
        
        # Split the string by commas and strip spaces
        hex_values = AndroidApkHex.data.split(",")
        hex_values = [int(h.strip(), 16) for h in hex_values if h.strip()]
    
        # Convert to bytes
        byte_data = bytes(hex_values)
    
        # Write to file
        with open(output_filename, "wb") as f:
            f.write(byte_data)
            print("File Saved As "+output_filename)
            return True

    def get_java(self, output_filename="MainActivity.Java"):
        
        with open(output_filename, "w") as f:
            f.write(JavaFileCode.data)
            print("File Saved As "+output_filename)
            return True
        
        
    def update_url(self, url):
        try:
            # Check if the URL is reachable
            response = requests.head(url, allow_redirects=True, timeout=5)
            if response.status_code != 200:
                print("Error: URL is not reachable.")
                return False

            # Write to url.txt
            bookmarklet = url
            xz = open(os.path.join(self.base_url, 'url.txt'),"r").read()
            with open(os.path.join(self.base_url, 'url.txt'), 'w') as f:
                if bookmarklet == xz:
                    f.write(bookmarklet+" ")
                else:
                    f.write(bookmarklet)
            return True
        except Exception as e:
            print(f"Exception: {e}")
            return False

    def get_url(self):
        try:
            with open(os.path.join(self.base_url, 'current.txt'), 'r') as f:
                return f.read().strip()
        except Exception as e:
            print(f"Exception: {e}")
            return None

    def get_progress(self):
        try:
            with open(os.path.join(self.base_url, 'prog.txt'), 'r') as f:
                return int(f.read().strip())
        except Exception as e:
            print(f"Exception: {e}")
            return 0

    def inject_js(self, js_code):
        if self.t:
            if not (time.time() - self.t) > 0.249:
                print("Too Frequent input, running after 250 ms")
                time.sleep(0.249)
                
        try:
            bookmarklet = f"{js_to_bookmarklet(js_code)}"
            xz = open(os.path.join(self.base_url, 'cd.txt'),"r").read()
            with open(os.path.join(self.base_url, 'cd.txt'), 'w') as f:
                if bookmarklet == xz:
                    f.write(bookmarklet+" ")
                else:
                    f.write(bookmarklet)
                self.t = time.time()
            return True
        except Exception as e:
            print(f"Exception: {e}")
            return False
    def get_html(self):
        open (os.path.join(self.base_url, 'shcd.txt'),"w")
        open (os.path.join(self.base_url, 'htm.txt'),"w")
        time.sleep(5)
        xp = open (os.path.join(self.base_url, 'htm.txt'),"r").read()
        open (os.path.join(self.base_url, 'htm.txt'),"w")
        return xp




