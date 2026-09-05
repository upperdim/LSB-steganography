# LSB-Steganography
Least significant bit image steganography.

Embeds secret images into host images and extracts them back. It may reduce quality of embedded secret images when their original size do not fit into the host image.

# Results
![Host Image: Zelda (512x512)](/examples/host_zelda512.png "Host Image: Zelda (512x512)")
<br>
Host Image: Zelda (512x512)

|              Lena                                                                           |                      Peppers                                                                       |
|:-------------------------------------------------------------------------------------------:|:--------------------------------------------------------------------------------------------------:|
|![](/examples/secret_lena256.png) <br> Secret Image 1: Lena (256x256)                        |  ![](/examples/secret_peppers256.png) <br> Secret Image 2: Peppers (256x256)                       |
|![](/examples/steg_zelda_lena512.png) <br> Stegano Image 1: Lena embedded in Zelda (512x512) | ![](/examples/steg_zelda_peppers512.png) <br> Stegano Image 2: Peppers embedded in Zelda (512x512) |
|![](/examples/extract_lena256.png) <br> Extracted Image 1: Lena (256x256)                    | ![](/examples/extract_peppers256.png) <br> Extracted Image 2: Peppers (256x256)                    |
