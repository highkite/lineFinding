# lineFinding

Algorithm to detect lines in images enhanced by some post-processing functionality.

The file **lineFinding.py** contains a very simple to use line finding algorithm that allows the extraction of lines
from images. In contrast to edge detectors (as, e.g., Canny, Sobel) is does not provide an image with emphasized
lines. It produces a set of lines that are defined by four points corresponding to their start- and end- points.

The file **postProcessing.py** provides two algorithms that allow to group detected lines with respect to their
mutual adjacency and the combination of lines with equal or similar slope.

# Installation
The linefinding algorithm needs the **numpy** library. It can be installed with pip:

```pip install numpy```

# Usage

Images must be given as numpy ***ndarray***. An easy way to achieve that is by using the **Skimage** library (http://scikit-image.org/).

```python
from skimage import io
image = io.imread(fileName, as_gray=True)
```

## Find lines in images

To find lines in images you need to specify what pixels are part of the line. This is done by checking
for every pixel its color and returning ***True***, if the pixel matchs the line color and ***False***
otherwise. 
An example for a function that can be applied on black images with white lines using the 
Skimage ***mean()*** method is given in the following:

```python
mean = image.mean()
def isLineColor(_color):
  return _color > mean
```

Now you can simply call the ***findLines*** method.

```python
import lineFinding
lines = lineFinding.findLines(image, isLineColor=isLineColor)
```

The list ***lines*** contains the extracted lines of the image in the format

```python
[numpyArray([x1_1,y1_1,x2_1,y2_1]),...,numpyArray([x1_n,y1_n,x2_n,y2_n])]
```
Thus it can be easily visualized using the **PyPlot** library.

You can also call the ***_findLines*** method that returns a set of ***LineSegment***s. A ***LineSegment***
is a datastructure that holds the characteristics of a single line.
The start- and end- points of a line can be accessed by
```python
x1 = lineSegment.x_start
y1 = lineSegment.y_start
x2 = lineSegment.x_end
y2 = lineSegment.y_end
```

## Apply post-processing

To improve the linefinding result or to extract more information you can apply some post processing steps.

### Group lines
It is possible to group lines into ***structure***s. A ***structure*** contains lines that are connected to each
other. This can be done as follows:
```python
import lineFinding
import postProcessing
...
lines = lineFinding._findLines(image, isLineColor=isLineColor)
structures = postProcessing.groupAdjacentLines(lines, delta=1)
```
Thereby the ***delta*** gives the neighbourhood in which a line is considered as adjacent. For ***delta=1*** we
check only the 3x3 neighbourhood of the start-and end point of a library.

### Combine lines with equal slope
As a further post processing step we can combine those lines that have an equal slope and are adjacent. You can
do so by typing:
```python
structures = postProcessing.combineLinesWithEqualSlope(structures, angle_epsilon=30, delta=1)
```
It is necessary to apply a grouping of lines first. As before the ***delta*** defines the considered 
neighbourhood-size. Two lines will be combined if the angle between them is ***(0/180) +- angle_epsilon***.

# Examples

In the following there are some example applications of the algorithms. The parameter ***delta*** was set to
***1*** and the ***angle_epsilon*** to ***50*** degree.

## Example 1
<table>
  <tr>
    <th>The input image</th>
    <th>After applying the grouping algorithm</th>
    <th>And than the combination of similar lines</th>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/highkite/lineFinding/master/documentation/images/sampleLineFinding_1.png" width="100"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/highkite/lineFinding/master/documentation/images/sampleLineFinding_1_group.png" width="250"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/highkite/lineFinding/master/documentation/images/sampleLineFinding_1_combine.png" width="250"></td>
  </tr>
</table>

## Example 2

<table>
  <tr>
    <th>The input image</th>
    <th>After applying the grouping algorithm</th>
    <th>And than the combination of similar lines</th>
  </tr>
  <tr>
    <td align="center"><img src="https://raw.githubusercontent.com/highkite/lineFinding/master/documentation/images/sampleLineFinding_3.png" width="100"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/highkite/lineFinding/master/documentation/images/sampleLineFinding_3_group.png" width="250"></td>
    <td align="center"><img src="https://raw.githubusercontent.com/highkite/lineFinding/master/documentation/images/sampleLineFinding_3_combine.png" width="250"></td>
  </tr>
</table>
