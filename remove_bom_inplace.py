import os, codecs, argparse

# copy-pasta from https://www.stefangordon.com/remove-bom-mark-from-text-files-in-python/
def remove_bom_inplace(path):
    """Removes BOM mark, if it exists, from a file and rewrites it in-place"""
    buffer_size = 4096
    bom_length = len(codecs.BOM_UTF8)
 
    with open(path, "r+b") as fp:
        chunk = fp.read(buffer_size)
        if chunk.startswith(codecs.BOM_UTF8):
            i = 0
            chunk = chunk[bom_length:]
            while chunk:
                fp.seek(i)
                fp.write(chunk)
                i += len(chunk)
                fp.seek(bom_length, os.SEEK_CUR)
                chunk = fp.read(buffer_size)
            fp.seek(-bom_length, os.SEEK_CUR)
            fp.truncate()


# main
parser = argparse.ArgumentParser()
parser.add_argument('--path', type=str, help='location of the csv to convert')

args = parser.parse_args()

remove_bom_inplace(args.path)