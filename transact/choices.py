
Domicile = (
    (u'U.S. citizen', u'United States citizen'),
    (u'U.S. resident', u'United States resident'),
    (u'non-resident', u'Non-resident'),
)

Domestic = (
    (u'domestic_account', u'Domestic'),
    (u'international_account', u'International'),
)


Resident_US = (
    (u'Yes', u'Yes'),
    (u'No', u'No'),
)

Citizen_US = (
    (u'Yes', u'Yes'),
    (u'No', u'No'),
)

Entity_Domicile = (
    (u'U.S. domicile', u'United States citizen'),
    (u'non-U.S.', u'United States resident'),
)

Entity_Type = (
    (u'revocable_trust', u'Revocable Trust'),
    (u'irrevocable', u'Irrevocable Trust'),
    (u'limited_parter', u'Limited Partnership'),
    (u'llc', u'LLC'),
    (u'corporation', u'Corporation'),
)

Syndicate = (
    (u'Yes', u'Yes'),
    (u'No', u'No'),
)

Associated_AC = (
    (u'Y', u'Yes'),
    (u'N', u'No'),
)

Associated_Person = (
    (u'Y', u'Yes'),
    (u'N', u'No'),
)

Financial_Advisor = (
    (u'yes', u'Yes'),
    (u'no', u'No'),
)

Owners_AI = (
    (u'Y', u'Yes'),
    (u'N', u'No'),
)

Invest_To = (
    (u'0', u'I will be investing for myself'),
    (u'1', u'I will investing on behalf of another person or entity'),
)

KYCstatus = (
    (u'Pending', u'Pending'),
    (u'Auto Approved', u'Auto Approved'),
    (u'Manual Approved', u'Manual Approved'),
    (u'Disapproved', u'Disapproved'),
)

AMLstatus = (
    (u'Pending', u'Pending'),
    (u'Auto Approved', u'Auto Approved'),
    (u'Manual Approved', u'Manual Approved'),
    (u'Disapproved', u'Disapproved'),
)

Approval_Status = (
    (u'Pending', u'Pending'),
    (u'Approved', u'Approved'),
    (u'Not Approved', u'Not Approved'),
)

Account_Type = (
    (u'individual', u'Individual'),
    (u'entity', u'Entity'),
    (u'tic', u'TIC'),
    (u'jtwros', u'JTWROS'),
    (u'ira', u'IRA'),
    (u'sepira', u'SepIRA'),
    (u'roth', u'ROTH'),
)

Risk_Profile = (
    (u'1', u'Very Conservative'),
    (u'2', u'Conservative'),
    (u'3', u'Hybrid'),
    (u'4', u'Aggressive'),
    (u'5', u'Very Aggressive'),
)

Investment_Experience = (
    (u'1', u'None'),
    (u'2', u'Little'),
    (u'3', u'Somewhat'),
    (u'4', u'Plenty'),
    (u'5', u'Extensive'),
)

Priv_Off_Experience = (
    (u'1', u'None'),
    (u'2', u'Little'),
    (u'3', u'Somewhat'),
    (u'4', u'Plenty'),
    (u'5', u'Extensive'),
)

Education = (
    (u'1', u'High School or GED'),
    (u'2', u'4 Year College or University'),
    (u'3', u'Graduate Degree'),
    (u'4', u'Other'),
    # (u'5', u'Extensive'),
)

Accredited_Status = (
    (u'Pending', u'Pending'),
    (u'Self Accredited', u'Self Accredited'),
    (u'Verified Accredited', u'Verified Accredited'),
    (u'Not Accredited', u'Not Accredited'),
)

Allow_Status = (
    (u'Pending', u'Pending'),
    (u'Income', u'Income'),
    (u'Assets', u'Assets'),
    (u'All Parties Accredited', u'All Parties Accredited'),
    # (u'5', u'Extensive'),
)

Issue_Type = (
    (u'1', u'Equity'),
    (u'2', u'Debt'),
    (u'3', u'Hybrid'),
    (u'4', u'Fund'),
)

Issue_Type = (
    (u'1', u'Equity'),
    (u'2', u'Debt'),
    (u'3', u'Hybrid'),
    (u'4', u'Fund'),
)

Trade_Type = (
    (u'ACH', u'ACH'),
    (u'WIRE', u'WIRE'),
    (u'CHECK', u'CHECK'),
)

External_Account_Type = (
    (u'Account', u'Account'),
    (u'Issuer', u'Issuer'),
)

Link_Type = (
    (u'owner', u'Owner'),
    (u'manager', u'Manager'),
)