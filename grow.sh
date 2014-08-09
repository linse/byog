DIR='gif_raw'
OUTDIR='gif_converted'
# TODO if dir does not exist or empty, leave script
mkdir -p $OUTDIR

for f in `ls $DIR`; do
  echo $DIR/$f;
	convert $DIR/$f -coalesce $OUTDIR/tmp.gif
  convert $OUTDIR/tmp.gif -resize 200% $OUTDIR/$f
done
rm $OUTDIR/tmp.gif


