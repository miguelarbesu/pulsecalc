#!/usr/bin/env bash
# -*- coding: utf-8 -*-

printf "Creating GitHub repository..."
gh repo create pulsecalc
git push --set-upstream origin main
