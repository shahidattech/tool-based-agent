import json
import os


sample_conversations = [
    
    {
      "role": "Customer",
      "message": "I’m Jane Doe.  I’m buying the Sante Fe",
      "inputs": {"identifier": "Shahid"}
    },
    {
      "role": "FI",
      "message": "Fantastic!  We appreciate the opportunity. Since you’re ready to buy, we’ll be finalizing all your paperwork after which you can take your new car home! 😀 We can go at your pace, but this likely won’t take more than 20 minutes to complete.",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "Ok great.",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "Jane, I need to send a code to the number we have on file for you in order to secure your information.  Please select the number that we should send the code to: \nXXX-XXX-4567\nXXX-XXX-6789\nXXX-XXX-0293",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "XXX-XXX-0293",
      "inputs": {"phone_number": "XXX-XXX-0293"} 
    },
    {
      "role": "FI",
      "message": "Ok Jane I've sent a code to your phone.  Please tell me the code.",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "1234",
      "inputs": {"otp": "1234"}
    },
    {
      "role": "FI",
      "message": "Perfect.  It looks like the sales team has entered all your information. \n\nCan you please confirm that this information is correct, and that this is your agreement with the sales department:\n\nFull Name as it appears on Driver's License: Jane Doe\nPhone / Address where vehicle will be registered: 555-555-0293 / 123 Oak Street, Rivertown, CA 90210\nCurrent Insurance policy Info including policy number, effective and expiration dates, and provider: Geico G09876543 effective 3/15/24 expiring 3/15/25\nVehicle selection including VIN, miles, Trim, and Color: 5XYZWDLB8JG512345 2023 Hyundai Santa Fe Limited Black 1,500 Miles\nTrade vehicle if applicable including VIN, miles, trim, and Color: 1GNSKBE0XBR123456 Chevrolet Tahoe LT 30,000 miles White\nSale price: $38000\nRebate amount if applicable: $1500\nDealer fees: $1100\nTrade value if applicable: $28000\nTrade payoff if applicable: $25000\nTax rate: 8.5%\nSocial Security number: 123456789 customer has 780 Experian score\nTime at address and whether rent/own? and payment?: 5 yrs, Rent, $2000 per month\nEmployment Info: Full-time, 6 years at XYZ Corporation, Senior Accountant\nMonthly income: $6000 monthly\nAgreement: Customer expects a payment below $700.",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "Yes that looks good.  And also I really want to finance with space coast.  They already quoted me a rate, so",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "Yes, of course you can finance with SCCU.  Are you open to other lenders if their rates are a bit lower?",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "No, I’ll just stick with SCCU",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "Well that keeps it easy for me. I appreciate it. 😀\n\nLet’s first get your DMV paperwork all signed, then I’ll show you some different options SCCU has available for your excellent credit.\n\nWe will apply your signature to the following documents: \nOdometer(s)\nSecure Power of Attorney (if trade)\nTitle Reassignment(s)\nPower of Attorney(s)\nStatement of tag intent\nPollution Statements(s)\nInsurance Declaration\nBill of Sale(s)\n\nPlease sign your name to apply your signature to those documents.",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "'signs name'",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "Thank you.  You may now select your financing option using Space Coast Credit Union as your lender.  You may select one of the following directly, or we can adjust according to your feedback.\n\nOption 1: Comprehensive Protection Package\n● Includes: GAP, Extended Warranty, Prepaid Maintenance, Tire and Wheel Coverage\n● Loan Term: 60 months\n● Interest Rate: 6.49%\n● Monthly Payment: $856.55\n\nOption 2: Moderate Protection Package\n● Includes: Gap, Extended Warranty, Prepaid Maintenance\n● Loan Term: 72 months\n● Interest Rate: 6.74%\n● Monthly Payment: $722.60\n\nOption 3: Budget Protection Package\n● Includes: GAP, Extended Warranty, Prepaid Maintenance, Tire and Wheel \n● Loan Term: 84 months\n● Interest Rate: 7.24%\n● Monthly Payment: $667\n\nPlease select, 1, 2, 3, or adjust.",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "Adjust I’m leaning toward option 2, but I think I just want the gap included and not the rest.",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "I'm glad you’ve decided to go with one of our option packages. You’re interested in GAP coverage but are thinking of skipping the warranty and maintenance. That makes sense and will obviously be a little less.\n\nBut just for a moment, if you don't mind, let’s go over why having the full package might be beneficial for you.",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "Sure, but I’m mainly concerned about keeping my payments low. The full package is a bit more than I planned.",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "I completely understand wanting to keep your payments manageable. Let's look at the numbers again. Currently, without the warranty and maintenance, the payment difference for 72 months is about $40. If you were to go with just the warranty, it’s around $27 less. Also, if you’d consider it, extending to 75 months makes the payment difference even closer.",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "Right, so it seems I will save some money by not getting the full package. Every dollar counts, ya know.",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "That’s true, but let’s consider what the full package includes and how it could save you money and hassle in the long run.\n\n1. Comprehensive Protection: With the warranty, any unexpected repairs are covered, saving you from potentially significant out-of-pocket expenses down the road. Car repairs can be costly, and having a warranty means you won't have to worry about those unexpected costs.\n2. Maintenance Coverage: Regular maintenance is crucial for keeping your vehicle in optimal condition. The maintenance package covers routine services like oil changes, tire rotations, and other essentials. This not only keeps your car running smoothly but also maintains its value over time.\n3. Peace of Mind: Having both the warranty and maintenance ensures that you’re fully protected against any surprises. You can drive with confidence knowing that both unexpected repairs and regular maintenance are covered.\n4. Convenient Financing: By extending your term to 75 months, the payment difference becomes even smaller. This way, you get comprehensive coverage for just a bit more each month. In fact, the slight increase might be more manageable than having to deal with large repair bills or maintenance costs unexpectedly.\n\nWhat do you think about those points - If the payment isn’t so much different, you’d like to have the protection, right?",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "Those are good points, but I’m still on the fence.",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "I understand. Think of it this way: It’s a small additional investment for substantial peace of mind and the possible savings in the future. Plus, you’ll enjoy the convenience of bundled services without worrying about extra costs.",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "That makes sense. The convenience and peace of mind are pretty appealing.",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "Exactly! Let’s ensure you’re fully covered and stress-free. The slight increase in your monthly payment is a worthwhile investment for the protection and peace of mind you’ll receive. Shall we go ahead with the full package? It’ll still be less than 700/month for sure at the slightly longer term. What do you say?",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "Alright, you’ve convinced me. Let’s do it.",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "Yes, I agree, let’s finish everything here and get you into your new car.  Please sign again your name so that we may apply your signatures to the following documents:\n\nDealer privacy notice\nCredit application \nRisk Based Pricing Notice\nOFAC/ID\nAftermarket contracts \nBuyers Order  \nLaw Finance Agreement\n\nIt is on the law agreement that you will see your payment of 699.31 for 75 months with SCCU.  Please sign your name:",
      "inputs": {}
    },
    {
      "role": "Customer",
      "message": "'signs name'",
      "inputs": {}
    },
    {
      "role": "FI",
      "message": "Next Steps : 1.Processing DMV:  Your registration has been transferred to your new vehicle, and the salesperson will transfer over your tag. 2.Finalizing Finance Documents: Space Coast will send you out a loan package once they complete funding. 3. Insurance: Please provide your insurance agent with the new vehicle information. 4. Enjoy your new car! 5. We can email your signed documents or print them for you, which would you prefer?",
      "inputs": {}
    }
]


def read_json_examples():
    # Get the directory of the current script
    current_dir = os.path.dirname(os.path.realpath(__file__))
    examples = None
    # Read the JSON file
    with open(os.path.join(current_dir, 'examples.json'), 'r') as file:
        examples = json.load(file)
    return examples

def serialize_doc(doc)-> dict:
    if isinstance(doc, dict):
        if "_id" in doc:
            doc["_id"] = str(doc["_id"])
        return doc
    if isinstance(doc, list):
        return [serialize_doc(d) for d in doc]

