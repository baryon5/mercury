from tornado.ioloop import IOLoop

from threading import Thread, main_thread
from queue import PriorityQueue, Empty

import time, os, types

from .languages import LANGUAGES
from subprocess import TimeoutExpired

class RunLoop(Thread):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.queue = PriorityQueue()

    def run(self):
        while main_thread().is_alive():
            try:
                priority, run, cb = self.queue.get(timeout=2)
                self._do_run(run)
                if cb:
                    if isinstance(cb, types.FunctionType):
                        IOLoop.current().add_callback(cb)
                    else:
                        if len(cb) < 3:
                            cb = (cb[0],cb[1],{})
                        IOLoop.current().add_callback(cb[0],*cb[1],**cb[2])
                self.queue.task_done()
            except Empty:
                pass

    def request_run(self,run,callback=None,priority=5):
        self.queue.put((priority,run,callback))
        
    def _do_run(self,run):
        lang = LANGUAGES[run.language.index]
        fn = run.main_file.path

        input_data = (run.problem.sample_input_data if
                      (run.is_a_test and run.problem.sample_input_data) else
                      run.problem.input_data)
        in_data = None
        if input_data:
            if run.problem.read_from_file:
                fd = open(os.path.join(os.path.dirname(fn),run.problem.read_from_file),"w")
                fd.write(input_data)
                fd.close()
            else:
                in_data = input_data

        code, out = lang.compile(fn)
        if code == 0:
            run.compiled_successfully = True
            try:
                before = time.time()
                code, out = lang.run(fn,input=in_data,timeout=run.problem.time_limit)
                after = time.time()
                run.runtime = (after - before) * 1000
            except TimeoutExpired as err:
                run.runtime = run.problem.time_limit * 1000
                code = -1
                out = "Execution time limit reached."
        else:
            run.compiled_successfully = False
        run.output = out
        run.exit_code = code

        if run.problem.auto_judge and (not run.is_a_test):
            if not run.compiled_successfully:
                run.judgement = "Failed to compile"
                run.score = 0
            elif code == -1:
                run.judgement = "Program execution time limit exceeded"
                run.score = 0
            elif code > 0:
                run.judgement = "Runtime/program error"
                run.score = 0
            else:
                if run.output.strip() == run.problem.expected_output.strip():
                    run.judgement = "Correct"
                    if run.time_to_submission:
                        run.score = round((run.problem.competition.original_time_left -
                                           run.time_to_submission) /
                                          run.problem.competition.original_time_left * 1000)
                    else:
                        run.score = 1000
                else:
                    run.judgement = "Incorrect"
                    run.score = 0

        run.has_been_run = True
        run.save()
