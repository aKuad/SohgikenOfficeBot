#
# boss.py
#

# Module import
## Standard & Extension modules
import requests
import json
import re
import sys

## Local modules
sys.path.append("./scmd/boss")
import boss_help
import boss_add
import boss_list
import boss_delete
import boss_print


# Function define
def boss(TOKEN_BEARER, datas):
  # Option check
  ## Variables initialize
  flag_ephe = False
  flag_smpl = False
  flag_bimg = False
  flag_subcHasRun = False
  var_intext = datas["text"]

  # When not empty imput, arguments check
  if datas["text"] != "":
    # Divide with space and loop
    for stt_txpart in datas["text"].split():
      # Sub command 'help'
      if stt_txpart == "help" or stt_txpart == "--help":
        boss_help.boss_help(TOKEN_BEARER, datas)
        flag_subcHasRun = True
        break

      # Sub command 'add'
      elif stt_txpart == "add" or stt_txpart == "a":
        var_intext = re.sub("^ *(add|a)", "", var_intext)
        var_intext = re.sub("^ *", "", var_intext)
        boss_add.boss_add(TOKEN_BEARER, datas, var_intext)
        flag_subcHasRun = True
        break

      # Sub command 'list'
      elif stt_txpart == "list" or stt_txpart == "l":
        boss_list.boss_list(TOKEN_BEARER, datas)
        flag_subcHasRun = True
        break

      # Sub command 'delete'
      elif stt_txpart == "delete" or stt_txpart == "d":
        var_intext = re.sub("^ *(delete|d)", "", var_intext)
        var_intext = re.sub("^ *", "", var_intext)
        boss_result.boss_result(TOKEN_BEARER, datas, var_intext)
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
      # Option 'big'

      elif stt_txpart == "-b" or stt_txpart == "--big":
        flag_bimg = True
        var_intext = re.sub("^ *(-b|--big)", "", var_intext)
        var_intext = re.sub("^ *", "", var_intext)

      # Other input
      else :
        break


  # Branch with sub command has run or not
  if flag_subcHasRun == False:
    boss_print.boss_print(TOKEN_BEARER, datas, flag_ephe, flag_smpl, flag_bimg)


  # Quit
  return
