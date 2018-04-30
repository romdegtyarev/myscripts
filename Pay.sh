#!/bin/bash

#Pay "file whith pay log"
#The amount is indicated in the last column
#Type of payment is indicated in the first column:
#Products                   PR
#Eating in the dining room  DPR
#A restaurant               RPR
#Household chemicals        Chem
#Payments                   PM
#Clothing                   CL
#Entertainment              ENT
#For home                   HM
#Health                     HLS

#Variables
script_name=$0
file=$1

NORMAL='\033[0m'
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[0;33m'
process=0

sum=0
max=0
pay_date_of_max=0
pay_date=0
strings_number=0
string=0

days=0
today=0
today_month=0

months_money=10000
days_money=310
real_days_money=0

PR=0
DPR=0
RPR=0
Chem=0
PM=0
CL=0
ENT=0
HM=0
HLS=0

#Start
if [[ $# -lt 1 ]]
	then
		echo "Enter name of file"
		exit 0
fi

#Сount the number of days before the end of the month
today=$(date \+"%d")
today_month=$(date \+"%m")
if [[ $today_month -eq 1 || $today_month -eq 3 || $today_month -eq 5\
                         || $today_month -eq 7 || $today_month -eq 8\
                         || $today_month -eq 10 || $today_month -eq 12 ]]
	then
		days=$((31-today))
elif [[ $today_month -eq 2 ]]
	then
		days=$((28-today))
else
		days=$((30-today))
fi

#Сount the number of strings in file
strings_number=$(wc $file | awk '{printf $1"\n"}')
#echo "$strings_number"
#Calculate the amount of costs for the last column
#Lines beginning with "*" are not considered
while [ "$strings_number" -ne 0 ]
do

	string=$(awk 'NR == '$strings_number'{print$1}' $file)
	if [[ $string != \** ]]
	then
#Analytics
		case $string in
			PR)
			string=$(awk 'NR == '$strings_number'{print $NF}' $file)
			PR=$((PR+string))
			;;
			DPR)
			string=$(awk 'NR == '$strings_number'{print $NF}' $file)
			DPR=$((DPR+string))
			;;
			RPR)
			string=$(awk 'NR == '$strings_number'{print $NF}' $file)
			RPR=$((RPR+string))
			;;
			Chem)
			string=$(awk 'NR == '$strings_number'{print $NF}' $file)
			Chem=$((Chem+string))
			;;
			PM)
			string=$(awk 'NR == '$strings_number'{print $NF}' $file)
			PM=$((PM+string))
			;;
			CL)
			string=$(awk 'NR == '$strings_number'{print $NF}' $file)
			CL=$((CL+string))
			;;
			ENT)
			string=$(awk 'NR == '$strings_number'{print $NF}' $file)
			ENT=$((ENT+string))
			;;
			HM)
			string=$(awk 'NR == '$strings_number'{print $NF}' $file)
			HM=$((HM+string))
			;;
			HLS)
			string=$(awk 'NR == '$strings_number'{print $NF}' $file)
			HLS=$((HLS+string))
			;;
		esac
#End of analytics
		string=$(awk 'NR == '$strings_number'{print $NF}' $file)
		if [[ string -gt max ]]
			then
				pay_date_of_max=${pay_date:0:2}
				pay_date_of_max=$((pay_date_of_max-1))
				pay_date_of_max="${pay_date_of_max}${pay_date:2}"
				max=$((string))
		fi
		#echo "Строка $strings_number: $string"
		sum=$((sum+string))
	else
		string=$(awk 'NR == '$strings_number'{print$2}' $file)
		if [[ $string == '*' ]]
			then
				pay_date=$(awk 'NR == '$strings_number'{print $NF}' $file)
		fi
	fi
	strings_number=$((strings_number-1))

done

#Output to file and screen
strings_number=$(wc $file | awk '{printf $1"\n"}')
string=$(awk 'NR == '$strings_number'{print$1}' $file)
if [[ $string == '***Сумма:' ]]
	then
		sed -i -e' '$strings_number'd ' $file
		echo "***Сумма: $sum***" >> $file
		echo "***Sum: $sum***"
		echo "***Max cost pay: $pay_date_of_max - $max"
		#Products                   PR
		echo -e "Products                   $PR\t$((PR*100/sum)) % \t\c"
		process=0
		if [[ $((PR*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((PR*100/sum)) -gt 25 && $((PR*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((PR*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Eating in the dining room  DPR
		echo -e "Eating in the dining room  $DPR\t$((DPR*100/sum)) % \t\c"
		process=0
		if [[ $((DPR*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((DPR*100/sum)) -gt 25 && $((DPR*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((DPR*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#A restaurant               RPR
		echo -e "A restaurant               $RPR\t$((RPR*100/sum)) % \t\c"
		process=0
		if [[ $((RPR*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((RPR*100/sum)) -gt 25 && $((RPR*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((RPR*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Household chemicals        Chem
		echo -e "Household chemicals        $Chem\t$((Chem*100/sum)) % \t\c"
		process=0
		if [[ $((Chem*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((Chem*100/sum)) -gt 25 && $((Chem*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((Chem*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Payments                   PM
		echo -e "Payments                   $PM\t$((PM*100/sum)) % \t\c"
		process=0
		if [[ $((PM*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((PM*100/sum)) -gt 25 && $((PM*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((PM*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Clothing                   CL
		echo -e "Clothing                   $CL\t$((CL*100/sum)) % \t\c"
		process=0
		if [[ $((CL*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((CL*100/sum)) -gt 25 && $((CL*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((CL*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Entertainment              ENT
		echo -e "Entertainment              $ENT\t$((ENT*100/sum)) % \t\c"
		process=0
		if [[ $((ENT*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((ENT*100/sum)) -gt 25 && $((ENT*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((ENT*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#For home                   HM
		echo -e "For home                   $HM\t$((HM*100/sum)) % \t\c"
		process=0
		if [[ $((HM*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((HM*100/sum)) -gt 25 && $((HM*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((HM*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Health                     HLS
		echo -e "Health                     $HLS\t$((HLS*100/sum)) % \t\c"
		process=0
		if [[ $((HLS*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((HLS*100/sum)) -gt 25 && $((HLS*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((HLS*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"

		echo "***Until the end of the month left $days days***"
else
		echo "***Сумма: $sum***" >> $file
		echo "***Sum: $sum***"
		echo "***Max cost pay: $pay_date_of_max - $max"
		#Products                   PR
		echo -e "Products                   $PR\t$((PR*100/sum)) % \t\c"
		process=0
		if [[ $((PR*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((PR*100/sum)) -gt 25 && $((PR*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((PR*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Eating in the dining room  DPR
		echo -e "Eating in the dining room  $DPR\t$((DPR*100/sum)) % \t\c"
		process=0
		if [[ $((DPR*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((DPR*100/sum)) -gt 25 && $((DPR*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((DPR*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#A restaurant               RPR
		echo -e "A restaurant               $RPR\t$((RPR*100/sum)) % \t\c"
		process=0
		if [[ $((RPR*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((RPR*100/sum)) -gt 25 && $((RPR*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((RPR*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Household chemicals        Chem
		echo -e "Household chemicals        $Chem\t$((Chem*100/sum)) % \t\c"
		process=0
		if [[ $((Chem*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((Chem*100/sum)) -gt 25 && $((Chem*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((Chem*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Payments                   PM
		echo -e "Payments                   $PM\t$((PM*100/sum)) % \t\c"
		process=0
		if [[ $((PM*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((PM*100/sum)) -gt 25 && $((PM*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((PM*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Clothing                   CL
		echo -e "Clothing                   $CL\t$((CL*100/sum)) % \t\c"
		process=0
		if [[ $((CL*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((CL*100/sum)) -gt 25 && $((CL*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((CL*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Entertainment              ENT
		echo -e "Entertainment              $ENT\t$((ENT*100/sum)) % \t\c"
		process=0
		if [[ $((ENT*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((ENT*100/sum)) -gt 25 && $((ENT*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((ENT*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#For home                   HM
		echo -e "For home                   $HM\t$((HM*100/sum)) % \t\c"
		process=0
		if [[ $((HM*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((HM*100/sum)) -gt 25 && $((HM*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((HM*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"
		#Health                     HLS
		echo -e "Health                     $HLS\t$((HLS*100/sum)) % \t\c"
		process=0
		if [[ $((HLS*100/sum)) -le 25 ]]
			then
			echo -e "${GREEN}[\c"
		elif [[ $((HLS*100/sum)) -gt 25 && $((HLS*100/sum)) -le 50 ]]
			then
			echo -e "${YELLOW}[\c"
		else
			echo -e "${RED}[\c"
		fi
		while [[ process -lt $((HLS*100/sum)) ]]
		do
			echo -e "-\c"
			process=$((process+1))
		done
		echo -e "]${NORMAL}"

		echo "***Until the end of the month left $days days***"
fi

#Warnings
real_days_money=$(((months_money-sum)/days))
if [[ real_days_money -ge $days_money ]]
	then
		echo -e "${GREEN}***Still good =)*** ${NORMAL}"
elif [[ $real_days_money -lt $days_money && $real_days_money -gt 0 ]]
	then
		echo -e "${YELLOW}***Not good =(***  ${NORMAL}"
else
		echo -e "${RED} ***Fucked up!*** ${NORMAL}"
fi

exit 0