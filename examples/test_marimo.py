import hyperspy.api as hs
import sys

# Mock marimo environment
sys.modules["marimo"] = object()

def main():
    roi = hs.roi.SpanROI(left=0, right=10)
    res = roi.gui(toolkit="anywidget", display=False)
    print("Marimo output:")
    print("Widget:", res["anywidget"]["widget"])
    print("wdict left:", res["anywidget"]["wdict"]["left"])
    print("wdict right:", res["anywidget"]["wdict"]["right"])

if __name__ == "__main__":
    main()
