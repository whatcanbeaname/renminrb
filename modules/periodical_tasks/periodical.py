# import time
from apscheduler.schedulers.blocking import BlockingScheduler
# from datetime import datetime
# from datetime import date

def start(job):
    sch = BlockingScheduler()

    # outputstr = 'this is good'
    # sch.add_job(job, "date", run_date=datetime(2021, 7, 27, 13, 51, 10), args=[outputstr])
    # sch.add_job(job, 'date', run_date=date(2021, 7, 28), args=['text'])

    # sch.add_job(job, "interval", seconds=3)
    # Schedule job_function to be called every two hours
    # sch.add_job(job, 'interval', hours=2)
    sch.add_job(job, 'interval', hours=48)
    # The same as before, but starts on 2010-10-10 at 9:30 and stops on 2014-06-15 at 11:00
    # sch.add_job(job, 'interval', hours=2, start_date='2021-07-10 09:30:00', end_date='2021-08-15 11:00:00')
    # Run the `job_function` every hour with an extra-delay picked randomly in a [-120,+120] seconds window.
    '''该选项使您能够在执行时间中添加随机组件。如果您拥有多个服务器，不希望它们在同一时刻运行作业，
    或者想要防止具有类似选项的多个作业始终同时运行，则这可能是有用的'''
    # sch.add_job(job, 'interval', hours=1, jitter=120)

    # Schedules job_function to be run on the third Friday
    # of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
    # sch.add_job(job, 'cron', month='6-8,11-12', day='3rd fri', hour='0-3')
    # Runs from Monday to Friday at 5:30 (am) until 2014-05-30 00:00:00
    # sch.add_job(job, 'cron', day_of_week='mon-fri', hour=5, minute=30, end_date='2014-05-30')

    # sch.add_job(job, 'cron', day_of_week='fri', hour=8, minute=30)
    sch.start()

'''
1. date触发器：
在某个日期时间只触发一次事件。示例代码如下：

2. interval触发器：
想要在固定的时间间隔触发事件。interval的触发器可以设置以下的触发参数：
weeks：周。整形。
days：一个月中的第几天。整形。
hours：小时。整形。
minutes：分钟。整形。
seconds：秒。整形。
start_date：间隔触发的起始时间。
end_date：间隔触发的结束时间。
jitter：触发的时间误差。

3. crontab触发器：
在某个确切的时间周期性的触发事件。可以使用的参数如下
year：4位数字的年份。
month：1-12月份。
day：1-31日。
week：1-53周。
day_of_week：一个礼拜中的第几天（ 0-6或者 mon、 tue、 wed、 thu、 fri、 sat、 sun）。
hour： 0-23小时。
minute： 0-59分钟。
second： 0-59秒。
start_date： datetime类型或者字符串类型，起始时间。
end_date： datetime类型或者字符串类型，结束时间。
timezone：时区。
jitter：任务触发的误差时间。
'''
