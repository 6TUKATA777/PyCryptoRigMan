from flask import Flask, jsonify
from flask_classy import FlaskView
import yaml

from .adapters.adapter_factory import AdapterFactory, AdapterType


class Rig(object):
    def __init__(self, config):
        self.data = dict()
        self.config = config
        adapter_type = AdapterType.__getattr__(str(self.config['adapter']).upper())
        self.adapter = AdapterFactory.create(adapter_type, self.config)

        # Function wrappers
        self.stats = dict()

    def update_stats(self):
        self.adapter.refresh()
        self.stats = {
            'name': self.config['name'],
            'address': self.config['address'],
            'adapter': self.config['adapter'],
            'hashrate': self.adapter.get_hashrate(),
        }

    def __str__(self):
        return str(jsonify(self.stats))


class RigMonitor(object):
    def __init__(self, config=None):
        if config is None:
            self.config = dict()
        else:
            self.load_config(config)
        self.rigs = []
        self.stats = dict()

    def add_rig(self, rig):
        print("Added rig '{0}'".format(rig.config['name']))
        self.rigs.append(rig)

    def update_stats(self):
        stats = dict()
        stats['rigs'] = []
        stats['hashrate'] = 0
        for rig in self.rigs:
            print(rig.stats)
            rig.update_stats()
            stats['rigs'].append(rig.stats)
            stats['hashrate'] += rig.stats['hashrate']

    def load_config(self, config: dict):
        self.config = config
        rigs = self.config['lwmon']['rigs']
        print(config)
        for rig_conf in rigs:
            rig = Rig(rig_conf)
            self.add_rig(rig)
            print(rig)