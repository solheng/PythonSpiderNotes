# -*- coding:utf-8 -*-

def auto_switch_frame(func):
    def wrapper(selector_str, *args, **kvargs):
        frame_id_list_list = analyze_element_frames(selector_str)

        if len(frame_id_list_list) != 1:
            raise Exception("找到" +str(len(frame_id_list_list)) + "个" + selector_str)

        for frame_id in frame_id_list_list[0]:
            solBrowser.switch_to.frame(frame_id)

        ret = None
        ret = func(selector_str, *args, **kvargs)
        try:
            for _ in frame_id_list_list[0]:
                solBrowser.switch_to.parent_frame()
        except Exception:
            logger.getlogger().warning("定位"+str(selector_str)+"后切回原frame失败")

        return ret
    return wrapper


def max_try(tries=5):
    """
    :param tries: 最多重试的次数。默认5次
    :return:
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            max_try_times = tries
            while max_try_times:
                max_try_times = max_try_times - 1
                try:
                    return f(*args, **kwargs)
                except Exception as e:
                    if max_try_times == 0:
                        raise e
                    logger.getlogger().error(str(e) + '继续重试')
                    time.sleep(0.5)
        return wrapper
    return decorator


def max_try_with_auto_switch_frame(tries=5):
    def decorator(f):
        @wraps(f)
        @auto_switch_frame
        def wrapper(selector_str, *args, **kwargs):
            max_try_times = tries
            while max_try_times:
                max_try_times = max_try_times - 1
                try:
                    return f(selector_str, *args, **kwargs)
                except Exception as e:
                    if max_try_times == 0:
                        raise e
                    logger.getlogger().info("忽略一次调用异常" + str(e))
                    time.sleep(0.5)
        return wrapper
    return decorator


def print_decorator(f):

    @wraps(f)
    def wrapper(*args, **kwargs):
        param_uuid = uuid.uuid1()
        logger.getlogger().info("now function name  : "+f.__name__)
        logger.getlogger().info("previous function name  : "+sys._getframe().f_back.f_code.co_name)
        if args:
            logger.getlogger().info("object  : "+str(args[0]))
            logger.getlogger().info("uuid : "+str(param_uuid)+", before params  : "+str(args[1:]) + str(kwargs))
        ret = f(*args, **kwargs)
        if args:
            logger.getlogger().info("object  : "+str(args[0]))
            logger.getlogger().info(logger.getlogger().info("uuid : "+str(param_uuid)+", return params  : "+str(ret)))
            logger.getlogger().info("uuid : "+str(param_uuid)+", after params  : "+str(args[1:]) + str(kwargs))
        return ret
    return wrapper
