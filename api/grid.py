from http.server import BaseHTTPRequestHandler
import png
import io
import cgi
from urllib.parse import parse_qs

def add_grid_to_image(image_bytes, line_width, line_space):
    reader = png.Reader(bytes=image_bytes)
    width, height, pixels, metadata = reader.read()
    
    pixel_data = list(pixels)
    
    planes = metadata['planes']
    
    for y in range(0, height, line_space):
        for line_offset in range(line_width):
            if y + line_offset < height:
                row = pixel_data[y + line_offset]
                for x in range(width):
                    if planes == 1:
                        row[x] = 0
                    elif planes == 2:
                        row[x * 2] = 0
                        row[x * 2 + 1] = 255
                    elif planes == 3:
                        row[x * 3] = 0
                        row[x * 3 + 1] = 0
                        row[x * 3 + 2] = 0
                    elif planes == 4:
                        row[x * 4] = 0
                        row[x * 4 + 1] = 0
                        row[x * 4 + 2] = 0
                        row[x * 4 + 3] = 255
    
    for x in range(0, width, line_space):
        for line_offset in range(line_width):
            if x + line_offset < width:
                for y in range(height):
                    row = pixel_data[y]
                    pixel_x = x + line_offset
                    if planes == 1:
                        row[pixel_x] = 0
                    elif planes == 2:
                        row[pixel_x * 2] = 0
                        row[pixel_x * 2 + 1] = 255
                    elif planes == 3:
                        row[pixel_x * 3] = 0
                        row[pixel_x * 3 + 1] = 0
                        row[pixel_x * 3 + 2] = 0
                    elif planes == 4:
                        row[pixel_x * 4] = 0
                        row[pixel_x * 4 + 1] = 0
                        row[pixel_x * 4 + 2] = 0
                        row[pixel_x * 4 + 3] = 255
    
    output = io.BytesIO()
    metadata.pop("physical")
    writer = png.Writer(width=width, height=height, **metadata)
    writer.write(output, pixel_data)
    return output.getvalue()

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        try:
            content_type = self.headers['content-type']
            if not content_type:
                self.send_error(400, 'Content-Type header is missing')
                return
            
            ctype, pdict = cgi.parse_header(content_type)
            if ctype == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                fields = cgi.parse_multipart(self.rfile, pdict)
                
                if 'image' not in fields:
                    self.send_error(400, 'Image file is required')
                    return
                
                image_data = fields['image'][0]
                line_width = int(fields.get('lineWidth', [1])[0])
                line_space = int(fields.get('lineSpace', [20])[0])
                
                result_image = add_grid_to_image(image_data, line_width, line_space)
                
                self.send_response(200)
                self.send_header('Content-Type', 'image/png')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.send_header('Content-Length', str(len(result_image)))
                self.end_headers()
                self.wfile.write(result_image)
            else:
                self.send_error(400, 'Content-Type must be multipart/form-data')
        except Exception as e:
            self.send_error(500, str(e))
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
