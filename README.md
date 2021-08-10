# renminrb


download articles in http://opinion.people.com.cn/GB/8213/353915/index.html
zip and send an email to receivers.


Before using the downloader, a formatted config
file should be prepared that contains:

```
sender:   # must provide
receiver: # must provide
subject:  # must provide
content:  # optional
attach_dir:  # optional
attach_name: # optional, but should be provided if attach_dir is given
mail_license: # must provide
```