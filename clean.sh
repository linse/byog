DIR='gif_raw'
OUTDIR='gif_clean'
# TODO if dir does not exist or empty, leave script
mkdir -p $OUTDIR

for f in `ls $DIR`; do
  if [ ! -f $OUTDIR/$f ]; then
    echo $DIR/$f
	  convert $DIR/$f -coalesce $OUTDIR/$f
  fi
done


