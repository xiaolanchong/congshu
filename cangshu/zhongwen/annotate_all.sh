for f in *.txt; do
    /usr/bin/python3 "~/project/python/chinese_annotation/annotate.py" "$f" "${f%.txt}.htm"
done