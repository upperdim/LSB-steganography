import cv2 as cv
import numpy as np
import math

def embed_get_files():
	print('Enter host image name with extension: ', end = '')
	host_image_name = input()
	host_image = cv.imread(host_image_name)
	#host_image = cv.imread('zelda512.png')

	print('Enter secret image name with extension: ', end = '')
	secret_image_name = input()
	secret_image = cv.imread(secret_image_name)
	#secret_image = cv.imread('lena256.png')

	print('Enter output image name: ', end = '')
	output_image_name = input()
	#output_image_name = 'stegano.png'

	output_image_name_check, output_image_extension = output_image_name.split('.')
	if output_image_name_check == 'jpeg' or output_image_name_check == 'jpg':
		output_image_name = output_image_name + '.png'
		print('Output file name changed to: ', output_image_name)

	# Check how many MSB's of secret image can be embedded given host images size
	hostrows,   hostcols,   hostchannels   = host_image.shape
	secretrows, secretcols, secretchannels = secret_image.shape

	max_msb = 8
	while (hostrows * hostcols < secretrows * secretcols * max_msb):
		max_msb -= 1

	if max_msb == 0:
		print('Error! max_msb = 0')
		exit(1)

	return host_image, secret_image, output_image_name, max_msb

def extract_get_files():
	print('Enter steganography image name with extension: ', end = '')
	steg_image = cv.imread( input() )
	#steg_image = cv.imread('stegano.png')

	print('Enter output image name: ', end = '')
	output_image_name = input()
	#output_image_name = 'extracted.png'

	output_image_name_check, output_image_extension = output_image_name.split('.')
	if output_image_name_check == 'jpeg' or output_image_name_check == 'jpg':
		output_image_name = output_image_name + '.png'
		print('Output file name changed to: ', output_image_name)

	return steg_image, output_image_name

def PSNR(original, compressed):
    mse = np.mean((original - compressed) ** 2)
    if(mse == 0):
        return 100
    max_pixel = 255.0
    psnr = 20 * math.log10(max_pixel / math.sqrt(mse))
    return psnr

def embed(host_image, secret_image, max_msb):
	hostrows,   hostcols,   hostchannels   = host_image.shape
	secretrows, secretcols, secretchannels = secret_image.shape

	if hostrows != 512 or hostcols != 512:
		print('Host image size should be 512x512')
		exit(1)

	if (secretrows != 256 or secretcols != 256):
		print('Secret image size should be 256x256')
		exit(1)

	curr_host_row = 0
	curr_host_col = 0

	for row in range(0, secretrows):
		for col in range(0, secretcols):
			r, g, b = secret_image[col, row]
			binval = '{0:08b}'.format(r)
			bin_MSBs = binval[0: max_msb: 1]

			for bit in bin_MSBs:
				hr, hb, hg = host_image[curr_host_col, curr_host_row]
				hostbinval = '{0:08b}'.format(hr)
				newbin = hostbinval[0: 7: 1] + bit
				new = int(newbin, 2)
				
				host_image[curr_host_col, curr_host_row] = (new, new, new)

				curr_host_col += 1
				if (curr_host_col == hostcols):
					curr_host_col = 0
					curr_host_row += 1

	return host_image

def extract(steg_image):
	max_msb = 4
	stegrows, stegcols, stegchannels = steg_image.shape

	if stegrows != 512 or stegcols != 512:
		print('Stegano image size should be 512x512')
		exit(1)

	new_img_layer = np.zeros((256, 256, 3), dtype = np.uint8)

	curr_new_img_row = 0
	curr_new_img_col = 0

	traveled_pixel_count = 0
	LSBs_buffer = ''

	for row in range(0, stegrows):
		for col in range(0, stegcols):
			sr, sb, sg = steg_image[col, row]
			binval = '{0:08b}'.format(sr)
			lsb = binval[7]
			LSBs_buffer += lsb
			traveled_pixel_count += 1

			if traveled_pixel_count % max_msb == 0:
				padding_size = 8 - max_msb
				for i in range(0, padding_size):
					LSBs_buffer += '0'

				dec_pixel_val = int(LSBs_buffer, 2)
				new_img_layer[curr_new_img_col, curr_new_img_row] = (dec_pixel_val, dec_pixel_val, dec_pixel_val)

				LSBs_buffer = ''

				curr_new_img_col += 1
				if curr_new_img_col == 256:
					curr_new_img_col = 0
					curr_new_img_row += 1

	return new_img_layer

def main():
	print('1 - Embed\n2 - Extract\nPlease enter mode: ', end = '')
	mode = input()

	while (mode != '1' and mode != '2'):
		print('Undefined input! Plase try again: ', end = '')
		mode = input()

	if (mode == '1'):
		host_image, secret_image, output_image_name, max_msb = embed_get_files()
		embedded_image = embed(host_image, secret_image, max_msb)
		cv.imwrite(output_image_name, embedded_image)
		print('PSNR: ', PSNR(host_image, embedded_image))

	if (mode == '2'):
		steg_image, output_image_name = extract_get_files()
		cv.imwrite(output_image_name, extract(steg_image))

if __name__ == '__main__':
	main()
