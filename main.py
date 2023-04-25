from flask import *
import uuid
import io

from sus_tools.event import *
from sus_tools.score import *
from sus_tools.sus_draw import *



app = Flask(__name__)


@app.route('/')
def index():
    return render_template('sus2svg.html')


@app.route('/generate', methods=['POST'])
def generate_svg():
    # たてよこ
    xy_type = request.args.get("type")
    susId = str(uuid.uuid4())

    susData = io.TextIOWrapper(io.BytesIO(request.get_data()))
    sus_lines = susData.readlines()
    sus = SUS(sus_lines)
    rebase = eventdump(sus_lines)

    sus.score = sus.score.rebase([
        Event(
            bar=event.get('bar'),
            bpm=event.get('bpm'),
            bar_length=event.get('barLength'),
            sentence_length=event.get('sentenceLength'),
            section=event.get('section'),
        )
        for event in rebase['events']
    ])


    if xy_type == "x":
        sus.export_xdraw(file_name=f"svgdata/{susId}.svg")
    if xy_type == "y":
        sus.export_ydraw(file_name=f"svgdata/{susId}.svg")

    return send_file(f"svgdata/{susId}.svg")
    

if __name__ == '__main__':
    app.run(debug=True, port=80, host="0.0.0.0")