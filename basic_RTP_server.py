import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst

# Initialize GStreamer
Gst.init(None)

# Create the GStreamer pipeline
pipeline = Gst.parse_launch(
    'filesrc location=video.mp4 ! decodebin ! x264enc ! rtph264pay ! udpsink host=127.0.0.1 port=5000'
)

# Start the pipeline (i.e., start streaming the video)
ret = pipeline.set_state(Gst.State.PLAYING)

if ret == Gst.StateChangeReturn.FAILURE:
    print("Failed to start the pipeline.")
elif ret == Gst.StateChangeReturn.NO_PREROLL:
    print("Pipeline started, but there is no data yet (live source?).")
else:
    print("Pipeline started successfully.")

# Wait until error or EOS (End of Stream)
bus = pipeline.get_bus()
msg = bus.timed_pop_filtered(Gst.CLOCK_TIME_NONE, Gst.MessageType.ERROR | Gst.MessageType.EOS)

if msg.type == Gst.MessageType.ERROR:
    err, debug = msg.parse_error()
    print(f"Error: {err}, {debug}")

# Free resources
pipeline.set_state(Gst.State.NULL)
