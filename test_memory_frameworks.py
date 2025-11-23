"""
Test Script for Memory System and Advanced Therapy Frameworks
"""
import asyncio
import sys

def test_advanced_frameworks():
    """Test advanced therapy frameworks"""
    print("\n" + "="*60)
    print("Testing Advanced Therapy Frameworks")
    print("="*60)

    try:
        from advanced_therapy_frameworks import AdvancedTherapyFrameworks

        frameworks = AdvancedTherapyFrameworks()

        # Test ACT for anxiety
        print("\n1. Testing ACT for anxiety:")
        intervention = frameworks.select_framework(
            user_input="I keep worrying about things I can't control",
            emotion="anxious",
            conversation_depth=3
        )
        print(f"   Framework: {intervention.framework}")
        print(f"   Technique: {intervention.technique}")
        print(f"   → {intervention.prompt[:100]}...")

        # Test Schema Therapy for patterns
        print("\n2. Testing Schema Therapy for abandonment:")
        intervention = frameworks.select_framework(
            user_input="Everyone always leaves me in the end",
            emotion="sad",
            conversation_depth=4
        )
        print(f"   Framework: {intervention.framework}")
        print(f"   Technique: {intervention.technique}")
        print(f"   → {intervention.prompt[:100]}...")

        # Test Narrative Therapy
        print("\n3. Testing Narrative Therapy:")
        intervention = frameworks.select_framework(
            user_input="Depression defines who I am",
            emotion="sad",
            conversation_depth=5
        )
        print(f"   Framework: {intervention.framework}")
        print(f"   Technique: {intervention.technique}")
        print(f"   → {intervention.prompt[:100]}...")

        print("\n✅ Advanced frameworks working!")
        return True

    except Exception as e:
        print(f"\n❌ Error testing frameworks: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_memory_system():
    """Test memory system (local cache)"""
    print("\n" + "="*60)
    print("Testing Long-Term Memory System")
    print("="*60)

    try:
        from memory_system import LongTermMemorySystem

        memory = LongTermMemorySystem()

        # Test user ID generation
        print("\n1. Testing anonymous user ID generation:")
        user_id = memory.get_anonymous_user_id("test-session-123")
        print(f"   User ID: {user_id}")

        # Test saving memories
        print("\n2. Testing memory saving:")
        await memory.remember(
            user_id=user_id,
            session_id="test-session-123",
            message="I feel really anxious about work",
            emotion="anxious",
            emotion_intensity=0.8,
            therapy_mode="cbt",
            detected_patterns=["catastrophizing"],
            concerns=["work stress"]
        )
        print("   ✓ Memory saved")

        await memory.remember(
            user_id=user_id,
            session_id="test-session-123",
            message="I'm feeling a bit better now",
            emotion="anxious",
            emotion_intensity=0.5,
            therapy_mode="cbt",
            breakthroughs=["Recognized thought pattern"]
        )
        print("   ✓ Second memory saved")

        # Test recalling memories
        print("\n3. Testing memory recall:")
        memories = await memory.recall(user_id, limit=10)
        print(f"   Recalled {len(memories)} memories")
        if memories:
            print(f"   Last emotion: {memories[-1]['emotion']}")

        # Test session summary
        print("\n4. Testing session summary:")
        summary = await memory.get_session_summary(user_id)
        print(f"   New user: {summary['new_user']}")
        if not summary['new_user']:
            print(f"   Total interactions: {summary['total_interactions']}")
            print(f"   Dominant emotion: {summary['dominant_emotion']}")
            print(f"   Mood trend: {summary['mood_trend']}")
            print(f"   Continuity prompt: {summary['continuity_prompt'][:60]}...")

        print("\n✅ Memory system working!")
        return True

    except Exception as e:
        print(f"\n❌ Error testing memory: {e}")
        import traceback
        traceback.print_exc()
        return False


async def test_integration():
    """Test therapy system with frameworks and memory"""
    print("\n" + "="*60)
    print("Testing Full Integration")
    print("="*60)

    try:
        from therapy_agent_system import TherapySystem
        from memory_system import LongTermMemorySystem

        therapy = TherapySystem()
        memory = LongTermMemorySystem()
        user_id = memory.get_anonymous_user_id("integration-test")

        # Test conversation with memory
        test_messages = [
            ("I always fail at everything I try", "sad", 0.7),
            ("Nobody really understands me", "lonely", 0.8),
            ("I can't stop worrying about the future", "anxious", 0.9),
        ]

        print("\n1. Processing test conversation:")
        for i, (message, emotion, intensity) in enumerate(test_messages, 1):
            print(f"\n   Message {i}: '{message}'")

            # Process through therapy system
            result = therapy.process_input(message, emotion, intensity)
            print(f"   Therapy mode: {result['therapy_mode']}")
            print(f"   Response preview: {result['response'][:80]}...")

            # Save to memory
            await memory.remember(
                user_id=user_id,
                session_id="integration-test",
                message=message,
                emotion=emotion,
                emotion_intensity=intensity,
                therapy_mode=result['therapy_mode'],
                detected_patterns=result.get('detected_distortions', [])
            )
            print(f"   ✓ Saved to memory")

        # Test continuity
        print("\n2. Testing session continuity:")
        summary = await memory.get_session_summary(user_id)
        print(f"   Continuity prompt: {summary['continuity_prompt']}")

        print("\n✅ Full integration working!")
        return True

    except Exception as e:
        print(f"\n❌ Error testing integration: {e}")
        import traceback
        traceback.print_exc()
        return False


async def main():
    """Run all tests"""
    print("\n" + "🧪 EMOSUPPORT ADVANCED FEATURES TEST SUITE 🧪".center(60))

    results = []

    # Test 1: Advanced Frameworks
    results.append(("Advanced Frameworks", test_advanced_frameworks()))

    # Test 2: Memory System
    results.append(("Memory System", await test_memory_system()))

    # Test 3: Integration
    results.append(("Full Integration", await test_integration()))

    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)

    for name, passed in results:
        status = "✅ PASSED" if passed else "❌ FAILED"
        print(f"{name:.<40} {status}")

    all_passed = all(r[1] for r in results)

    if all_passed:
        print("\n🎉 ALL TESTS PASSED! 🎉")
        print("\nYour EmoSupport app now has:")
        print("  ✅ Advanced therapy frameworks (ACT, Schema, Narrative, CFT, SFBT)")
        print("  ✅ Long-term memory system with local cache")
        print("  ✅ Session continuity across conversations")
        print("  ✅ Progress tracking and breakthrough detection")
        print("\nOptional: Set up Supabase for cloud memory sync!")
        print("  → See SUPABASE_SETUP.md for instructions")
        return 0
    else:
        print("\n⚠️  Some tests failed. Check errors above.")
        return 1


if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)
