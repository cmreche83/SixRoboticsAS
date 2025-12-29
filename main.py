import yaml


class ProjectPlan:
    def __init__(self, yaml_path, debug=False):
        self.debug = debug
        self.plan = []
        self.yaml = yaml_path
        self.__processed_jobs__ = []
        self.__unprocessed_jobs__ = []

    def __display_stack__(self, opt_loc: str = ""):
        """ """
        print(f"\n\n{opt_loc}\n")
        print("\t__display_stack__()")
        print(f"\tplan : {self.plan}")
        print(f"\t__processed_jobs__ : {self.__processed_jobs__}")
        print(f"\t__unprocessed_jobs__: {self.__unprocessed_jobs__}")
        print("\n\033[0m")

    def parser(self, file_path: str) -> dict:
        """parser(file_path:str)

        file_path:str string indicating the path of a yaml file

        returns a dictionary representation of the yaml file
        """
        with open(file_path, "r") as f:
            jobs = yaml.full_load(f)
        if self.debug:
            print(jobs)
        return jobs

    def no_dependencies_jobs_processor(self):
        """
        no_dependencies_joobs_processor()

        selects all jobs that do not have dependencies, 
        append them in a list and append that list to self.plan
        
        only jobs without dependencies can be considered 
        for the very first slot in a project plan.

        updates __processed_jobs__ and __unprocessed_jobs__
        to keep track of what has been processed
        versus what still requires to be processed

        In case no job without dependency is found in the yaml file : 
        raises a RuntimeError exception
        """
        no_dependencies = []
        for job in self.yaml_jobs:
            if self.yaml_jobs[job] is None:
                no_dependencies.append(job)
            elif "dependencies" not in self.yaml_jobs[job]:
                no_dependencies.append(job)
            else:
                self.__unprocessed_jobs__.append(job)
        if len(no_dependencies) > 0:
            self.plan.append(no_dependencies)
            # self.__processed_jobs__.append(*no_dependencies)
            self.__processed_jobs__ = [j for j in no_dependencies]
        else:
            raise RuntimeError(
                "\033[41mNo job/task found without dependencies\
 - most likely some jobs definition are missing from the yaml file\033[0m"
            )

        if self.debug:
            self.__display_stack__("\033[33mno_dependencies_jobs_processor()")

    def dependencies_jobs_processor(self):
        """
        append jobs to self.plan 
        while making sure their dependencies have been met
        
        in case jobs are left with missing dependencies 
        raise a RuntimeError 
        This can be because
        - unmet dependency : 
            one of the dependencies does not correspond 
            to a defined job in the yaml file
        - mutual dependency
        - mistake in the yaml file 
            (which did not make the parser fail 
            but make this method fails)
            
        if it runs fine, 
        self.plan should be in its final form after this step
        """
        if self.debug:
            print(f"\033[33mdependencies_jobs_processor()\n\033[0m")

        current_job_dependencies_met = []
        jobs_to_append = []
        nb_unprocessed = int(len(self.__unprocessed_jobs__))

        # goes through the list of unprocessed jobs
        for job in self.__unprocessed_jobs__:
            try:
                for dep in self.yaml_jobs[job]["dependencies"]:
                    # if dependency met, append it to the list of jobs with met dependencies
                    if dep in self.__processed_jobs__:
                        current_job_dependencies_met.append(dep)
                        if self.debug:
                            print(f"\033[33m\t{job} {dep} met\033[0m")
                    # else stop/break iterating through dependencies ( and will go through the next job - outer for loop )
                    else:
                        if self.debug:
                            print(f"\033[33m\t{job} break\033[0m")
                        break

                if len(self.yaml_jobs[job]["dependencies"]) == len(
                    current_job_dependencies_met
                ):
                    jobs_to_append.append(job)
                    if self.debug:
                        print(f"\033[32m\t{job} all dependencies met, job added\033[0m")
                        print(f"\033[33m\t__________\033[0m")
                else:
                    if self.debug:
                        print("\n")
                        print(
                            f"\033[31m\tUnmet dependencies remaining for {job}\033[0m"
                        )
                        print(
                            f"\033[33m\tDependencies required:\
                             {self.yaml_jobs[job]["dependencies"]}\033[0m"
                         )
                        print(
                            f"\033[33m\tDependencies found at this stage:\
                             {current_job_dependencies_met}\033[0m"
                        )
                # clears dependencies_met buffer before next job/loop iteration
                current_job_dependencies_met = []
            except TypeError:
                raise RuntimeError(
                    f"\033[41mError Occured while processing the following job : {job}\
 - Please check your yaml file\033[0m"
                )
                # raise RuntimeError(f"Error Occured while processing the following job : {job} - Please check your yaml file")
        self.plan.append(jobs_to_append)

        # move job from unprocessed to processed
        for job in jobs_to_append:
            self.__unprocessed_jobs__.remove(job)
            self.__processed_jobs__.append(job)

        if self.debug:
            self.__display_stack__("\t\033[33m")

        # checks if we still have unprocessed jobs in the list
        if int(len(self.__unprocessed_jobs__)) > 0:
            # if this amount has changed since last iteration/recursion of this function -> recurse on more time
            if nb_unprocessed != int(len(self.__unprocessed_jobs__)):
                if self.debug:
                    print(
                        f"\033[33m\n\tnb_unprocessed vs len(self.__unprocessed_jobs__):\
                        {nb_unprocessed} vs {int(len(self.__unprocessed_jobs__))}\033[0m\n"
                    )
                    print(f"\033[34m\n\tNew Iteration needed\033[0m\n")
                self.dependencies_jobs_processor()
            # if it has not changed (but still have unprocessed jobs)-> raise an Exception to alert the user we have an unmet dependency
            else:
                # this means that one of the dependency is not defined in the yaml file
                raise RuntimeError(
                    f"\033[41mThe following jobs have unmet or mutual dependencies :\
 {self.__unprocessed_jobs__}\033[0m"
                )

        # "else"
        # I do not have any unprocessed jobs left hence I do not need to run/recurse this function on more time

    def run(self):
        """
        Should be the only method the user calls
        
        calls 
        the parser, 
        no_dependencies_jobs_processor 
        and dependencies_jobs_processor
        returns plan ( an list containing lists of jobs )
        """
        try:
            self.yaml_jobs = self.parser(self.yaml)  # move it to a run fx
        except:
            raise RuntimeError(
                f"\033[41mFailed to parse the following yaml file : {self.yaml}\
 - Please check if path provided is valid and if the yaml file itself is valid\033[0m"
            )

        self.no_dependencies_jobs_processor()
        self.dependencies_jobs_processor()
        return self.plan



if __name__ == "__main__":
    #myproject = ProjectPlan("yaml/test_jobs.yaml", True)
    myproject = ProjectPlan("yaml/test_jobs.yaml")
    value = myproject.run()
    print(value)
