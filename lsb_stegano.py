import cv2 as cv
import numpy as np
import math


def embed_get_files():
	host_image_name = input('Enter host image  with extension: ')
	host_image = cv.imread(host_image_name)
	#host_image = cv.imread('zelda512.png')

	secret_image_name = input('Enter secret image  with extension: ')
	secret_image = cv.imread(secret_image_name)
	#secret_image = cv.imread('lena256.png')

	output_image_name = input('Enter output image  without extension: ')
	#output_image_name = 'stegano.png'

	output_image_name_check, output_image_extension = output_image_name.split('.')
	if output_image_extension == 'jpeg' or output_image_extension == 'jpg':
		output_image_name = output_image_name_check + '.png'
		print('Output file  changed to: ', output_image_name)

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
	steg_image = cv.imread( input('Enter steganography image  with extension: ') )
	#steg_image = cv.imread('stegano.png')

	output_image_name = input('Enter output image : ')
	#output_image_name = 'extracted.png'

	output_image_name_check, output_image_extension = output_image_name.split('.')
	if output_image_extension == 'jpeg' or output_image_extension == 'jpg':
		output_image_name = output_image_name_check + '.png'
		print('Output file  changed to: ', output_image_name)

	return steg_image, output_image_name


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

	for row in range(secretrows):
		for col in range(secretcols):
			r, g, b = secret_image[col, row]
			binval = '{0:08b}'.format(r)
			bin_MSBs = binval[0: max_msb: 1]  # TODO: remove :1

			for bit in bin_MSBs:
				hr, hb, hg = host_image[curr_host_col, curr_host_row]
				hostbinval = '{0:08b}'.format(hr)
				newbin = hostbinval[0: 7: 1] + bit  # TODO: remove :1
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

	for row in range(stegrows):
		for col in range(stegcols):
			sr, sb, sg = steg_image[col, row]
			binval = '{0:08b}'.format(sr)
			lsb = binval[7]
			LSBs_buffer += lsb
			traveled_pixel_count += 1

			if traveled_pixel_count % max_msb == 0:
				padding_size = 8 - max_msb
				for i in range(padding_size):
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
	mode = input('1 - Embed\n2 - Extract\nPlease enter mode: ')

	while (mode != '1' and mode != '2'):
		mode = input('Undefined input! Plase try again: ')

	if (mode == '1'):
		host_image, secret_image, output_image_name, max_msb = embed_get_files()
		embedded_image = embed(host_image, secret_image, max_msb)
		cv.imwrite(output_image_name, embedded_image)

	if (mode == '2'):
		steg_image, output_image_name = extract_get_files()
		cv.imwrite(output_image_name, extract(steg_image))


if __name__ == '__main__':
	main()
