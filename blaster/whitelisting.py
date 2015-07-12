
# curl -XDELETE '127.0.0.1:9200/20150712/article/_query?q=newspaper:vice'
# curl -XDELETE '127.0.0.1:9200/20150712/article/restaurant_report_konyvbar_in_budapest

# curl '127.0.0.1:9200/_cat/indices?v' | sort -rnk2
# curl '127.0.0.1:9200/_cat/indices?v' | sort -rnk2 | grep "20150[678].*"

# curl '127.0.0.1:9200/_nodes/settings?pretty=true'
# curl '127.0.0.1:9200/_count'
# curl '127.0.0.1:9200/20150712/article/_search?q=newspaper:theguardian&size=1000'


if __name__ == "__main__":
  pass