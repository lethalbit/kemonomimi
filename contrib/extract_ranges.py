#!/bin/python3
# This utility downloads the Unicode data mapping and uses it to
# generate ranges for specific categories of characters

from pathlib        import Path
from urllib.request import urlretrieve
from tempfile       import gettempdir
from argparse       import ArgumentParser, ArgumentDefaultsHelpFormatter
from io             import StringIO, SEEK_SET

DATAFILE_URL = 'https://www.unicode.org/Public/UNIDATA/UnicodeData.txt'


UNICODE_CATEGORIES = (
	'Cc', 'Cf', 'Co', 'Cs', 'Ll', 'Lm', 'Lo', 'Lt',
	'Lu', 'Mc', 'Me', 'Mn', 'Nd', 'Nl', 'No', 'Pc',
	'Pd', 'Pe', 'Pf', 'Pi', 'Po', 'Ps', 'Sc', 'Sk',
	'Sm', 'So', 'Zl', 'Zp', 'Zs'
)

def collapse(codepoints):
	size = len(codepoints)
	idx = 0
	while idx < size:
		low = codepoints[idx]
		while idx < size - 1 and codepoints[idx] + 1 == codepoints[idx + 1]:
			idx += 1

		high = codepoints[idx]
		span = high - low
		if span >= 2:
			yield (low, high)
		elif span == 1:
			yield (low, )
			yield (high, )
		else:
			yield (low, )
		idx += 1


def generate_table(codepoints, cols):
	buffer = StringIO()

	for _ in range(cols):
		buffer.write(f'|{"":23}')
	buffer.write('|\n')
	for _ in range(cols):
		buffer.write(f'|{"-"*23}')
	buffer.write('|\n')

	while True:
		row = list((c for _, c in zip(range(cols), codepoints)))

		if len(row) == 0:
			break

		for cell in row:
			buffer.write(f'| `{cell.replace(" ", ""):19}` ')
		rem = cols - len(row)
		if rem > 0:
			for _ in range(rem):
				buffer.write(f'|{"":23}')

		buffer.write('|\n')

	return buffer.getvalue()

def generate_kemonomimi(codepoints, cols):
	buffer = StringIO()

	while True:
		row = list((c for _, c in zip(range(cols), codepoints)))

		if len(row) == 0:
			break

		for cell in row:
			buffer.write(f' {cell.replace(" ", ""):19} |')
		buffer.write('\n')

	buffer.seek(buffer.tell() - 2, SEEK_SET)
	buffer.write(';\n')

	return buffer.getvalue()

def extract(args):

	data_file = Path(gettempdir()) / 'unicode_data.txt'
	if not data_file.exists():
		print('Downloading Unicode Data')
		urlretrieve(DATAFILE_URL, data_file)

	with data_file.open('r') as f:
		entries = map(str.lstrip, f.readlines())

	entries = list(entries)

	categories = args.category

	print(f'Collecting codepoint ranges for the categories {", ".join(categories)}')
	codepoints = map(
		lambda p: f'U+{p[0]:06X} ... U+{p[1]:06X}' if len(p) == 2 else f'U+{p[0]:06X}',
		collapse(list(map(
			lambda l: int(l.split(';')[0], 16),
			filter(
				lambda l: l.split(';')[2] in categories,
				entries
			)
		)))
	)

	if args.table:
		result = generate_table(codepoints, args.cols)
	elif args.kemonomimi:
		result = generate_kemonomimi(codepoints, args.cols)
	else:
		result = ' | '.join(list(codepoints))

	if args.output is not None:
		with args.output.resolve().open('w') as f:
			f.write(result)
	else:
		print(result)


def main():
	parser = ArgumentParser(
		formatter_class = ArgumentDefaultsHelpFormatter,
		description     = 'Unicode codepoint range extractor',
	)

	parser.add_argument(
		'-c', '--category',
		choices  = UNICODE_CATEGORIES,
		required = True,
		nargs    = '+'
	)

	parser.add_argument(
		'-o', '--output',
		type = Path,
		help = 'Output File (optional: will print to stdout if not specified)'
	)

	parser.add_argument(
		'-t', '--table',
		action  = 'store_true',
		default = False,
		help    = 'Generate a markdown table with the codepoints in it'
	)

	parser.add_argument(
		'-k', '--kemonomimi',
		action  = 'store_true',
		default = False,
		help    = 'Generate a Kemonomimi rule with the codepoints in it'
	)

	parser.add_argument(
		'-C', '--cols',
		type    = int,
		default = 4,
		help    = 'Number of columns to make the markdown table'
	)

	args = parser.parse_args()

	extract(args)

if __name__ == '__main__':
	main()
