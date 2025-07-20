#!/usr/bin/env python3
"""
Kiro + Strands Learning Path Navigator
Interactive guide to help you choose and start the right course
"""

import os
import sys
import subprocess

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    print("🚀 Kiro IDE + Strands SDK Learning Hub")
    print("=" * 50)
    print()

def show_course_options():
    print("📚 Choose Your Learning Path:")
    print()
    print("1. 🚀 2-Hour Quickstart Course")
    print("   • Perfect for: Rapid prototyping and exploration")
    print("   • Time: 2 hours")
    print("   • Level: Beginner")
    print("   • Outcome: Working AI agent demo")
    print()
    print("2. 📚 5-Day Comprehensive Workshop")
    print("   • Perfect for: Production-ready expertise")
    print("   • Time: 40 hours (5 days)")
    print("   • Level: Intermediate to Advanced")
    print("   • Outcome: Professional certification")
    print()
    print("3. 🤔 Help Me Choose")
    print("   • Compare courses side-by-side")
    print("   • Decision framework")
    print("   • Personalized recommendations")
    print()
    print("4. ❓ Just Browse")
    print("   • Explore all materials")
    print("   • No commitment needed")
    print()

def get_user_choice():
    while True:
        try:
            choice = input("Enter your choice (1-4): ").strip()
            if choice in ['1', '2', '3', '4']:
                return int(choice)
            else:
                print("Please enter 1, 2, 3, or 4")
        except KeyboardInterrupt:
            print("\n\nGoodbye! 👋")
            sys.exit(0)

def open_file(filepath):
    """Open file with default system application"""
    try:
        if sys.platform.startswith('darwin'):  # macOS
            subprocess.run(['open', filepath])
        elif sys.platform.startswith('linux'):  # Linux
            subprocess.run(['xdg-open', filepath])
        elif sys.platform.startswith('win'):  # Windows
            os.startfile(filepath)
        else:
            print(f"Please manually open: {filepath}")
    except Exception as e:
        print(f"Could not open file automatically. Please open: {filepath}")

def handle_quickstart():
    clear_screen()
    print_header()
    print("🚀 2-Hour Quickstart Course Selected!")
    print()
    print("Next steps:")
    print("1. ✅ Setup your environment (30 min)")
    print("2. 🎯 Follow the implementation guide (120 min)")
    print("3. 🧪 Use code templates for practice")
    print("4. 🏆 Complete assessment for certification")
    print()
    
    choice = input("Ready to start? (y/n): ").lower().strip()
    if choice == 'y':
        print("\n📂 Opening quickstart materials...")
        open_file("2hr-quickstart/README.md")
        print("✅ Check your file browser for the quickstart guide!")
    else:
        print("No problem! Materials are in the '2hr-quickstart' folder when you're ready.")

def handle_comprehensive():
    clear_screen()
    print_header()
    print("📚 5-Day Comprehensive Workshop Selected!")
    print()
    print("⚠️  Important Prerequisites:")
    print("• Completed 2-hour quickstart OR 6+ months Python experience")
    print("• 40 hours available for dedicated learning")
    print("• AWS account with Bedrock access")
    print("• Serious commitment to mastering AI agents")
    print()
    
    ready = input("Do you meet these prerequisites? (y/n): ").lower().strip()
    if ready == 'y':
        print("\n📂 Opening comprehensive workshop materials...")
        open_file("5day-comprehensive/README.md")
        print("✅ Check your file browser for the comprehensive guide!")
    else:
        print("\n💡 Recommendation: Start with the 2-hour quickstart first!")
        retry = input("Would you like to try the quickstart instead? (y/n): ").lower().strip()
        if retry == 'y':
            handle_quickstart()

def handle_comparison():
    clear_screen()
    print_header()
    print("🤔 Course Comparison & Decision Guide")
    print()
    print("Opening detailed comparison guide...")
    open_file("course-comparison.md")
    print("✅ Check your file browser for the comparison guide!")
    print()
    input("Press Enter to return to main menu...")

def handle_browse():
    clear_screen()
    print_header()
    print("📁 Browse All Materials")
    print()
    print("Available directories:")
    print("• 2hr-quickstart/ - Fast-track learning materials")
    print("• 5day-comprehensive/ - Deep expertise materials")
    print("• course-comparison.md - Help choosing your path")
    print()
    print("Feel free to explore at your own pace!")
    input("Press Enter to return to main menu...")

def main():
    while True:
        clear_screen()
        print_header()
        show_course_options()
        
        choice = get_user_choice()
        
        if choice == 1:
            handle_quickstart()
        elif choice == 2:
            handle_comprehensive()
        elif choice == 3:
            handle_comparison()
        elif choice == 4:
            handle_browse()
        
        print()
        continue_choice = input("Would you like to return to the main menu? (y/n): ").lower().strip()
        if continue_choice != 'y':
            break
    
    print("\n🎉 Happy learning! Build amazing AI agents! 🤖")
    print("💬 Need help? Check the support info in each course README")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
        sys.exit(0)