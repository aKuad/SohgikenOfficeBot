# coding=UTF-8
#
# gikentips.py
#

# Module import
## Standard & Extension modules
import requests
import json
import re
import sys

## Local modules
sys.path.append("./scmd/gikentips")
import gikentips_help
import gikentips_add
import gikentips_list
import gikentips_delete
import gikentips_print


# Function define
def gikentips(TOKEN_BEARER, datas):
  # Option check
  ## Variables initialize
  flag_ephe = False
  flag_smpl = False
  flag_subcHasRun = False
  var_intext = datas["text"]

  # When not empty imput, arguments check
  if datas["text"] != "":
    # Divide with space and loop
    for stt_txpart in datas["text"].split():
      # Sub command 'help'
      if stt_txpart == "help" or stt_txpart == "--help":
        gikentips_help.gikentips_help(TOKEN_BEARER, datas)
        flag_subcHasRun = True
        break

      # Sub command 'add'
      elif stt_txpart == "add" or stt_txpart == "a":
        var_intext = re.sub("^ *(add|a)", "", var_intext)
        var_intext = re.sub("^ *", "", var_intext)
        gikentips_add.gikentips_add(TOKEN_BEARER, datas, var_intext)
        flag_subcHasRun = True
        break

      # Sub command 'list'
      elif stt_txpart == "list" or stt_txpart == "l":
        gikentips_list.gikentips_list(TOKEN_BEARER, datas)
        flag_subcHasRun = True
        break

      # Sub command 'delete'
      elif stt_txpart == "delete" or stt_txpart == "d":
        var_intext = re.sub("^ *(delete|d)", "", var_intext)
        var_intext = re.sub("^ *", "", var_intext)
        gikentips_delete.gikentips_delete(TOKEN_BEARER, datas, var_intext)
        flag_subcHasRun = True
        break

      # Option 'ephemeral'
      elif stt_txpart == "-e" or stt_txpart == "--ephemeral":
        flag_ephe = True
        var_intext = re.sub("^ *(-e|--ephemeral)", "", var_intext)
        var_intext = re.sub("^ *", "", var_intext)

      # Option 'simple'
      elif stt_txpart == "-s" or stt_txpart == "--simple":
        flag_smpl = True
        var_intext = re.sub("^ *(-s|--simple)", "", var_intext)
        var_intext = re.sub("^ *", "", var_intext)

      # Other input
      else :
        break


  # Branch with sub command has run or not
  if flag_subcHasRun == False:
    gikentips_print.gikentips_print(TOKEN_BEARER, datas, flag_ephe, flag_smpl)


  # Quit
  return
