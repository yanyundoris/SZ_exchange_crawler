# 深交所上市公司与公告爬虫

爬取深交所上市公司列表以及公告

## 1. 爬取最新深交易所主板上市公司

见`Crawler_Companylist.py`.
 
### Function List 

 `Get_update_date`: Get the date info publishing
 
 `Get_total_page`: Get total page and current page from request text.
 
 `Get_table_from_page`: Parse table elements from requests'text.
 
 `Parse_table_row`: Parse rows in table returned.
 
 `Get_next_page`: Get next page request text.
 
 
 ## 2. 爬取自2015年1月1日起所有公告
 
见`Crawler_Notice.py`

### Function List:

`Get_all_company_code`: Load all company id.

`Get_notice_type`: Load all notice type id.

`Get_post_formfield`: Prepare a form data for sending request.

`Get_post_header`: Prepare a header for sending request.

`Parse_notice_html`: Parse notice returned.
 
