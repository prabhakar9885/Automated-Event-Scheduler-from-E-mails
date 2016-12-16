#
#	python source,py "TestFile.txt" "OutputFileName"
#

echo "Configuring the Stanford NER..."
export STANFORDTOOLSDIR="."
export CLASSPATH="$STANFORDTOOLSDIR/stanford-ner-2015-12-09/stanford-ner.jar"
export STANFORD_MODELS="$STANFORDTOOLSDIR/stanford-ner-2015-12-09/classifiers"

echo "Doing NER..."
echo "Target file: $1"
echo "Output file: $2"
python source.py $1 $2

echo "Done."