# Copyright (c) Facebook, Inc. and its affiliates.
#
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
from pathlib import Path
from utils.register import registry
from typing import Callable, List, Optional, Union
import json,copy

def get_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--scenario", default="Law.Scenario.Fact",
        choices=["Law.Scenario.Fact", "Law.Scenario.CollaborativeFact"],
        type=str)
    

    args, _ = parser.parse_known_args()

    scenario_group = parser.add_argument_group(
            title="Scenario",
            description="scenario configuration",
        )
    registry.get_class(args.scenario).add_parser_args(scenario_group) 
    args, _ = parser.parse_known_args()

    # Add args of patient to parser. 
    if hasattr(args, "plaintiff"):
        # subparsers = parser.add_subparsers(dest='class_name', required=True)
        plaintiff_group = parser.add_argument_group(
            title="Plaintiff",
            description="Plaintiff configuration",
        )
        if registry.get_class(args.plaintiff) is not None:
            # print("patient_name:", registry.get_class(args.patient).__name__)
            registry.get_class(args.plaintiff).add_parser_args(plaintiff_group)
        else:
            raise RuntimeError()
        
    # Add args of doctor to parser.
    if hasattr(args, "lawyer"):
        lawyer_group = parser.add_argument_group(
            title="Lawyer",
            description="Lawyer configuration",
        )
        if registry.get_class(args.lawyer) is not None:
            registry.get_class(args.lawyer).add_parser_args(lawyer_group)
        else:
            raise RuntimeError()
    
    # Add args of patient to parser.
    if hasattr(args, "supervisor"):
        # subparsers = parser.add_subparsers(dest='class_name', required=True)
        supervisor_group = parser.add_argument_group(
            title="Supervisor",
            description="Supervisor configuration",
        )
        if registry.get_class(args.supervisor) is not None:
            # print("patient_name:", registry.get_class(args.patient).__name__)
            registry.get_class(args.supervisor).add_parser_args(supervisor_group)
        else:
            raise RuntimeError()

    # Add args of patient to parser.
    if hasattr(args, "reporter"):
        reporter_group = parser.add_argument_group(
            title="Reporter",
            description="Reporter configuration",
        )
        if registry.get_class(args.reporter) is not None:
            registry.get_class(args.reporter).add_parser_args(reporter_group)
        else:
            raise RuntimeError()
    
    # Add args of host to parser.
    if hasattr(args, "host"):
        host_group = parser.add_argument_group(
            title="Host",
            description="Host configuration",
        )
        if registry.get_class(args.host) is not None:
            registry.get_class(args.host).add_parser_args(host_group)
        else:
            raise RuntimeError()

    args, _ = parser.parse_known_args()

    if hasattr(args, "doctor_database"):
        doctors = json.load(open(args.doctor_database))
        doctors_args = []
        for i, doctor in enumerate(doctors):
            doctor_parser = copy.deepcopy(parser)
            doctor_args, _ = doctor_parser.parse_known_args()
            doctor_group = doctor_parser.add_argument_group(
                title="Doctors",
                description="Doctor configuration",
            )
            vars(doctor_args).update(doctor)

            registry.get_class(doctor_args.doctor_name).add_parser_args(doctor_group)
            doctor_args = doctor_parser.parse_args()
            vars(doctor_args).update(doctor)
            doctors_args.append(doctor_args)

        setattr(args, "doctors_args", doctors_args)
    args, _ = parser.parse_known_args()
    # 遍历 Namespace 对象的属性并打印
    for arg_name in vars(args):
        print(f"{arg_name}: {getattr(args, arg_name)}")

    return args

