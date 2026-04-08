/// Modelo de usuario. Ref: Solution Design, DB Schema p.12 — tabla USERS.
class User {
  final int userId;
  final String name;
  final String surname;
  final DateTime birthdate;
  final String email;
  final DateTime createdAt;

  const User({
    required this.userId,
    required this.name,
    required this.surname,
    required this.birthdate,
    required this.email,
    required this.createdAt,
  });

  factory User.fromJson(Map<String, dynamic> json) => User(
        userId: json['user_id'] as int,
        name: json['name'] as String,
        surname: json['surname'] as String,
        birthdate: DateTime.parse(json['birthdate'] as String),
        email: json['email'] as String,
        createdAt: DateTime.parse(json['created_at'] as String),
      );

  Map<String, dynamic> toJson() => {
        'user_id': userId,
        'name': name,
        'surname': surname,
        'birthdate': birthdate.toIso8601String().split('T').first,
        'email': email,
        'created_at': createdAt.toIso8601String(),
      };
}
